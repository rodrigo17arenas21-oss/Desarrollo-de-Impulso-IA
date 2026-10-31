import reflex as rx
import json
import shutil
import subprocess
import unittest
from app.browser_scripts import BROWSER_SCRIPT
from test_browser_campaigns import BrowserCampaignTests


@unittest.skipUnless(
    shutil.which("node"),
    "Node absent : tests JavaScript omis, pas de test navigateur réel",
)
class PreferencesTests(unittest.TestCase):
    def test_preferences_persistence_errors_and_new_form_isolation(self):
        fixture = BrowserCampaignTests().fixture()
        harness = """
const assert=require('node:assert/strict');
const listeners={};
global.window={addEventListener(){}};
global.document={addEventListener(name,fn){listeners[name]=fn;}};
const storage=new Map();
global.localStorage={getItem(k){return storage.has(k)?storage.get(k):null;},setItem(k,v){storage.set(k,v);},removeItem(k){storage.delete(k);}};
"""
        checks = """
const api=window.ImpulsoBrowser, key='impulso.preferences.v1';
const prefs=(...args)=>JSON.parse(api.preferences(...args));
assert.equal(prefs('read').values.tono,'Cercano');
const p={version:1,tono:'Profesional',red_social:'LinkedIn'};
assert.equal(prefs('save',p).ok,true);
assert.deepEqual(prefs('read').values,p);
api.write([c]);const historyBefore=storage.get('impulso.campaigns.v1');
const blank={...c.campaign,nombre_negocio:'',tipo_negocio:'',producto:'',publico:'',objetivo:''};
let first=JSON.parse(api.prepareForm(blank,true,''));
assert.equal(first.values.tono,'Profesional');assert.equal(first.values.red_social,'LinkedIn');
// Capture an unsent form, navigate to settings and return without replacing it.
const draft={...blank,nombre_negocio:'Borrador sin enviar',tono:'Divertido',red_social:'WhatsApp'};
global.FormData=class {constructor(){}get(k){return draft[k];}};
listeners.input({target:{closest(){return {};}}});
assert.equal(prefs('save',{version:1,tono:'Inspirador',red_social:'Facebook'}).ok,true);
assert.deepEqual(JSON.parse(api.prepareForm(blank,false,'')).values,draft);
// A restored campaign is not changed by preferences or an unrelated draft.
assert.deepEqual(JSON.parse(api.prepareForm(c.campaign,false,c.id)).values,c.campaign);
assert.equal(JSON.parse(api.prepareForm(blank,true,'')).values.tono,'Inspirador');
// Even an empty in-progress form keeps its previous choices.
prefs('save',p);
assert.equal(JSON.parse(api.prepareForm(blank,false,'')).values.tono,'Inspirador');
const previous=storage.get(key);
assert.equal(prefs('save',{...p,tono:'Unknown'}).ok,false);assert.equal(storage.get(key),previous);
storage.set(key,'{broken');assert.equal(prefs('read').ok,false);
assert.equal(prefs('save',p).ok,false);assert.equal(storage.get(key),'{broken');
assert.equal(prefs('reset').ok,true);assert.equal(prefs('read').values.red_social,'Instagram');
assert.equal(storage.get('impulso.campaigns.v1'),historyBefore);
storage.set(key,JSON.stringify({...p,version:2}));assert.equal(prefs('read').ok,false);
const get=localStorage.getItem,set=localStorage.setItem,remove=localStorage.removeItem;
localStorage.getItem=()=>{const e=new Error('disabled');e.name='SecurityError';throw e;};
assert.match(prefs('read').error,/bloquea/);
assert.match(JSON.parse(api.prepareForm(blank,true,'')).notice,/bloquea/);
localStorage.getItem=get;
localStorage.removeItem=()=>{const e=new Error('disabled');e.name='SecurityError';throw e;};
assert.equal(prefs('reset').ok,false);localStorage.removeItem=remove;prefs('reset');
localStorage.setItem=()=>{const e=new Error('full');e.name='QuotaExceededError';throw e;};
assert.match(prefs('save',p).error,/espacio/);assert.equal(storage.has(key),false);
localStorage.setItem=set;
// Persistence across a fresh script instance (new session), not just module variables.
window.ImpulsoBrowser=null;
"""
        js = f"{harness}\n{BROWSER_SCRIPT}\nconst c={json.dumps(fixture)};\n{checks}\n{BROWSER_SCRIPT}\nassert.equal(JSON.parse(window.ImpulsoBrowser.preferences('read')).values.tono,'Cercano');"
        result = subprocess.run(
            ["node", "-e", js], capture_output=True, text=True, timeout=20
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
