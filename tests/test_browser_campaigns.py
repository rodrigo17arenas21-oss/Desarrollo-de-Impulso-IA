import reflex as rx
import unittest
import json
import shutil
import subprocess
from app.browser_scripts import BROWSER_SCRIPT
from app.generation import publication_text
from app.states.browser_state import script_call


class BrowserCampaignTests(unittest.TestCase):
    def fixture(self) -> dict:
        return {
            "version": 1,
            "id": "id-1",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-02T00:00:00Z",
            "campaign": {
                "nombre_negocio": "Café <Sol>",
                "tipo_negocio": "Cafetería",
                "producto": "Pan",
                "publico": "Vecinos",
                "objetivo": "Recibir consultas",
                "oferta": "",
                "precio": "",
                "tono": "Cercano",
                "red_social": "Instagram",
                "formato": "cuadrado",
            },
            "texts": {
                "headline_1": "Conoce Café <Sol>",
                "headline_2": "Mi edición\ncon saltos",
                "headline_3": "Consulta sobre Pan",
                "copy": "Texto personalizado",
                "description": "Pan para vecinos",
                "cta": "Envíanos un mensaje",
                "hashtags": "#CafeSol",
                "promotion_idea": "Propuesta pendiente de aprobación",
            },
            "selected_headline": "headline_2",
            "promotion_confirmed": True,
            "promotion_terms": "Dos panes por 50 MXN.",
            "pending_terms": "Otra propuesta sin confirmar",
            "pending_approved": False,
            "content_ready": True,
            "visual": {
                "template": "editorial",
                "format": "cuadrado",
                "headline": "Texto gráfico independiente",
                "subtext": "Texto secundario independiente",
                "background": "#242668",
                "foreground": "#FFFFFF",
                "accent": "#EF755D",
                "initialized": "true",
            },
        }

    @unittest.skipUnless(
        shutil.which("node"),
        "Node no disponible: acciones de historial no ejecutadas",
    )
    def test_real_history_buttons_and_save_conflict(self):
        harness = """
const assert=require('node:assert/strict');
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.events={};this.textContent='';this.dataset={};this.hidden=false;}
  append(...nodes){this.children.push(...nodes);}
  prepend(...nodes){this.children.unshift(...nodes);}
  replaceChildren(...nodes){this.children=nodes;}
  addEventListener(name,fn){this.events[name]=fn;}
  setAttribute(){} focus(){} remove(){}
  querySelector(tag){return this.children.find(n=>n.tag===tag);}
  click(){return this.events.click?.();}
}
const roots={'history-root':new Element('div'),'browser-status':new Element('p'),'designer-root':new Element('div'),'restore-history-campaign':new Element('button')};
let restoreClicks=0;roots['restore-history-campaign'].events.click=()=>restoreClicks++;
global.window={addEventListener(){},confirm(){return true;}};
global.document={addEventListener(){},getElementById(id){return roots[id]||null;},createElement(tag){return new Element(tag);},fonts:{ready:new Promise(()=>{})}};
let serial=0;global.crypto={randomUUID(){return 'copy-'+(++serial);}};
let stored=null;global.localStorage={getItem(){return stored;},setItem(k,v){stored=v;}};
function all(node){return [node,...node.children.flatMap(all)];}
function click(root,text){const n=all(roots[root]).find(n=>n.tag==='button'&&n.textContent===text);assert.ok(n,text);return n.click();}
"""
        assertions = """
(async()=>{
const api=window.ImpulsoBrowser;
api.write([c]);await api.history();
click('history-root','Abrir');assert.equal(restoreClicks,1);
const opened=JSON.parse(api.consumeOpen());assert.deepEqual(opened.texts,c.texts);
assert.throws(()=>api.consumeOpen(),/seleccionó/);
click('history-root','Duplicar');await Promise.resolve();
assert.equal(api.read().length,2);const copy=api.read().find(x=>x.id!==c.id);
assert.deepEqual(copy.texts,c.texts);assert.notEqual(copy.created_at,c.created_at);
await api.history();click('history-root','Eliminar');
let confirmation=all(roots['history-root']).find(n=>n.tag==='div'&&n.children.some(x=>x.textContent==='Sí, eliminar'));
assert.equal(confirmation.hidden,false);click('history-root','Cancelar');assert.equal(confirmation.hidden,true);assert.equal(api.read().length,2);
click('history-root','Eliminar');click('history-root','Sí, eliminar');await Promise.resolve();assert.equal(api.read().length,1);
api.write([c]);api.receive(c);api.designer(c);
click('designer-root','Guardar / actualizar campaña');assert.equal(api.read().length,1);
assert.match(roots['browser-status'].textContent,/actualizada/);
let external=api.read();external[0].updated_at='2099-01-01T00:00:00Z';api.write(external);const before=stored;
click('designer-root','Guardar / actualizar campaña');assert.equal(stored,before);assert.match(roots['browser-status'].textContent,/otra pestaña/);
click('designer-root','Guardar como copia');assert.equal(api.read().length,2);
// A stale delete must not remove a campaign updated in another tab.
api.write([c]);await api.history();external=api.read();external[0].updated_at='2099-01-01T00:00:00Z';api.write(external);
click('history-root','Eliminar');click('history-root','Sí, eliminar');assert.equal(api.read().length,1);assert.match(roots['browser-status'].textContent,/cambió/);
stored='{bad';await api.history();assert.ok(all(roots['history-root']).some(n=>n.textContent==='Volver a intentar'));assert.equal(stored,'{bad');
})().catch(e=>{console.error(e);process.exitCode=1;});
"""
        js = f"{harness}\n{BROWSER_SCRIPT}\nconst c={json.dumps(self.fixture())};\n{assertions}"
        result = subprocess.run(
            ["node", "-e", js], capture_output=True, text=True, timeout=20
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(
        shutil.which("node"), "Node no disponible: montaje DOM no ejecutado"
    )
    def test_delayed_dom_mount_and_bounded_failure(self):
        harness = """
const assert=require('node:assert/strict');
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.attributes={};}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=nodes;}
  setAttribute(key,value){this.attributes[key]=value;}
}
const roots={'browser-status':new Element('p')};
let ticks=0, mountAt=3, target='history-root', reads=0, writes=0;
global.window={addEventListener(){}};
global.document={addEventListener(){},getElementById(id){return roots[id]||null;},createElement(tag){return new Element(tag);}};
global.crypto={randomUUID(){return 'new-id';}};
global.localStorage={getItem(){reads++;return null;},setItem(){writes++;}};
// Advance a virtual clock, mounting only during a scheduled retry.
global.setTimeout=(callback,ms)=>{assert.equal(ms,50);queueMicrotask(()=>{ticks++;if(ticks===mountAt)roots[target]=new Element('div');callback();});};
"""
        assertions = """
(async()=>{
const api=window.ImpulsoBrowser;
const history=api.history();
assert.equal(reads,0,'Storage must not be read before the DOM exists');
assert.equal(roots['history-root'],undefined);
await history;
assert.equal(ticks,3);
assert.match(roots['history-root'].children[0].textContent,/Todavía no hay campañas guardadas/);
assert.match(roots['browser-status'].textContent,/0 campañas/);
// Direct designer visit without session data must offer useful next steps.
ticks=0;target='designer-root';mountAt=4;
c.id='';c.content_ready=false;c.campaign.nombre_negocio='';c.texts.headline_1='';
const designer=api.designer(c);
assert.equal(roots['designer-root'],undefined);
await designer;
assert.equal(ticks,4);
assert.match(roots['designer-root'].children[0].textContent,/No hay una campaña/);
assert.ok(roots['designer-root'].children.some(n=>n.href==='/historial'));
assert.ok(roots['designer-root'].children.some(n=>n.href==='/crear?nueva=1'));
assert.equal(writes,0);
// Never-mounted roots reject after a bounded number of retries.
for(const [id,operation] of [['history-root',()=>api.history()],['designer-root',()=>api.designer(c)]]) {
  delete roots[id];ticks=0;mountAt=-1;
  await assert.rejects(operation(),/No se pudo preparar/);
  assert.equal(ticks,100);
  assert.equal(roots['browser-status'].attributes.role,'alert');
}
// The on_load wrapper must return the failure to its Reflex callback.
ticks=0;
const failure=JSON.parse(await eval(wrapped));
assert.match(failure.mount_error,/historial/);
assert.equal(ticks,100);
// Retrying after a failure succeeds as soon as the root appears.
ticks=0;target='history-root';mountAt=2;
assert.equal(JSON.parse(await eval(wrapped)).ok,true);
assert.equal(ticks,2);
// Tool-script load failures also reach the callback instead of rejecting.
delete window.ImpulsoBrowser;ticks=0;mountAt=-1;
assert.match(JSON.parse(await eval(wrapped)).mount_error,/herramientas locales/);
assert.equal(ticks,100);
})().catch(e=>{console.error(e);process.exitCode=1;});
"""
        wrapped = script_call(
            "window.ImpulsoBrowser.history()", report_errors=True
        )
        js = f"{harness}\n{BROWSER_SCRIPT}\nconst c={json.dumps(self.fixture())};\nconst wrapped={json.dumps(wrapped)};\n{assertions}"
        result = subprocess.run(
            ["node", "-e", js], capture_output=True, text=True, timeout=20
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_serialized_fixture_preserves_edits_and_publication_approval(self):
        original = self.fixture()
        restored = json.loads(json.dumps(original, ensure_ascii=False))
        self.assertEqual(restored, original)
        publication = publication_text(
            restored["texts"],
            restored["selected_headline"],
            restored["promotion_terms"],
            restored["promotion_confirmed"],
        )
        self.assertEqual(
            publication,
            "Mi edición\ncon saltos\n\nTexto personalizado\n\n"
            "Dos panes por 50 MXN.\n\nEnvíanos un mensaje\n\n#CafeSol",
        )
        self.assertNotIn(restored["pending_terms"], publication)
        self.assertNotIn(restored["texts"]["promotion_idea"], publication)
        self.assertNotIn(restored["visual"]["headline"], publication)

    @unittest.skipUnless(
        shutil.which("node"),
        "Node no disponible: pruebas del navegador pendientes",
    )
    def test_browser_storage_validation_and_wrapping(self):
        fixture = self.fixture()
        javascript = """
const assert=require('node:assert/strict');
global.window={addEventListener(){}};
global.document={addEventListener(){}};
let stored=null;
global.localStorage={getItem(){return stored;},setItem(k,v){stored=v;}};
"""
        assertions = """
const api=window.ImpulsoBrowser;
assert.equal(api.valid(c),true);
assert.deepEqual(api.read(),[]);
api.write([c]);
assert.deepEqual(api.read()[0],c);
assert.throws(()=>api.write([c,c]),/duplicados/);
assert.equal(api.read().length,1);
const before=stored;
const missing={version:1,campaign:{},texts:{}};
assert.equal(Boolean(api.valid(missing)),false);
assert.throws(()=>api.write([missing]));
assert.equal(stored,before);
assert.deepEqual(api.read()[0],c);
const bad=JSON.parse(JSON.stringify(c));bad.visual.accent='url(javascript:alert(1))';
assert.equal(api.valid(bad),false);
assert.throws(()=>api.write([bad]));
assert.equal(stored,before);
assert.deepEqual(api.read()[0],c);
bad.visual.accent='#EF755D';bad.visual.image='https://external/image.png';
assert.equal(api.valid(bad),false);
stored='{broken';assert.throws(()=>api.read(),/JSON/);assert.equal(stored,'{broken');
stored=JSON.stringify({version:1,campaigns:[c,c]});assert.throws(()=>api.read(),/formato/);
localStorage.setItem=()=>{const e=new Error('quota');e.name='QuotaExceededError';throw e;};
assert.throws(()=>api.write([c]),/quota/);
localStorage.getItem=()=>{const e=new Error('disabled');e.name='SecurityError';throw e;};
assert.throws(()=>api.read(),/disabled/);
const ctx={measureText(s){return {width:Array.from(s).length*10};}};
assert.deepEqual(api.lines(ctx,'hola mundo',50),['hola','mundo']);
assert.deepEqual(api.lines(ctx,'abcdef',30),['abc','def']);
assert.deepEqual(api.lines(ctx,'uno\\ndos',100),['uno','dos']);
"""
        javascript = f"{javascript}\n{BROWSER_SCRIPT}\nconst c={json.dumps(fixture)};\n{assertions}"
        result = subprocess.run(
            ["node", "-e", javascript],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
