import reflex as rx

BROWSER_SCRIPT = r"""
(() => {
  if (window.ImpulsoBrowser) return;
  const KEY = 'impulso.campaigns.v1';
  const PREF_KEY = 'impulso.preferences.v1';
  const defaults = {version:1,tono:'Cercano',red_social:'Instagram'};
  let formDraft = null, formOwner = '', formStarted = false;
  function validPreferences(p) {
    return p && p.version === 1 && ['Cercano','Profesional','Inspirador','Divertido'].includes(p.tono) && ['Instagram','Facebook','WhatsApp','LinkedIn'].includes(p.red_social);
  }
  function preferences(action, values) {
    try {
      if(action === 'reset') {
        localStorage.removeItem(PREF_KEY);
        return JSON.stringify({ok:true,values:defaults,notice:'Valores iniciales restablecidos. Tu historial y tu campaña actual no cambiaron.'});
      }
      const raw=localStorage.getItem(PREF_KEY);
      if(action === 'save') {
        if(!validPreferences(values))throw new Error('Selecciona preferencias válidas.');
        if(raw!==null && !validPreferences(JSON.parse(raw)))throw new Error('Preferencias dañadas. Restablece solo las preferencias antes de guardar.');
        localStorage.setItem(PREF_KEY,JSON.stringify(values));
        return JSON.stringify({ok:true,values,notice:'Preferencias guardadas en este navegador. Se aplican solo a campañas nuevas.'});
      }
      const p=raw===null?defaults:JSON.parse(raw);
      if(!validPreferences(p))throw new Error('Preferencias incompatibles. Restablece solo las preferencias; el historial se conserva.');
      return JSON.stringify({ok:true,values:p,notice:raw===null?'Todavía no hay preferencias guardadas. Usamos Cercano e Instagram.':'Preferencias locales cargadas.'});
    }catch(e){return JSON.stringify({ok:false,error:e instanceof SyntaxError?'Preferencias dañadas. Restablece solo las preferencias; tu historial se conserva.':message(e)});}
  }
  function prepareForm(c, isNew, owner) {
    let values=clone(c), notice='';
    if(isNew){formDraft=null;formStarted=false;formOwner=owner;}
    if(formDraft && formOwner===owner && !isNew)values=clone(formDraft);
    else if(!formStarted && !owner && !businessKeys.filter(k=>!['tono','red_social','formato'].includes(k)).some(k=>c[k].trim())) {
      const result=JSON.parse(preferences('read'));
      if(result.ok){values.tono=result.values.tono;values.red_social=result.values.red_social;}
      else notice=result.error+' Se usan los valores iniciales. Puedes cambiar el tono y la red aquí.';
    }
    formStarted=true;formOwner=owner;formDraft=clone(values);
    return JSON.stringify({values,notice});
  }
  function captureForm(e) {
    const form=e.target.closest('#campaign-form');if(!form)return;
    const data=new FormData(form);formDraft=Object.fromEntries(businessKeys.map(k=>[k,String(data.get(k)||'')]));
  }
  document.addEventListener('input',captureForm);
  document.addEventListener('change',captureForm);
  document.addEventListener('submit',e=>{if(e.target.id==='campaign-form') {captureForm(e);formDraft=null;formStarted=false;}});
  const businessKeys = ['nombre_negocio','tipo_negocio','producto','publico','objetivo','oferta','precio','tono','red_social','formato'];
  const textKeys = ['headline_1','headline_2','headline_3','copy','description','cta','hashtags','promotion_idea'];
  const templates = [['editorial','Editorial','Titular protagonista y fotografía al pie.'],['split','Encuentro','Fotografía arriba y mensaje en bloque.'],['frame','Marco','Marco gráfico, fotografía y mensaje centrado.']];
  const colors = {background:'#242668',foreground:'#FFFFFF',accent:'#EF755D'};
  let current = null, pendingOpen = null, dirty = false, imageBusy = false, epoch = 0;
  const clone = x => JSON.parse(JSON.stringify(x));
  const color = x => typeof x === 'string' && /^#[0-9a-f]{6}$/i.test(x);
  function valid(c) {
    return c && c.version === 1 && typeof c.id === 'string' && c.id.length > 0 &&
      typeof c.created_at === 'string' && Number.isFinite(Date.parse(c.created_at)) &&
      typeof c.updated_at === 'string' && Number.isFinite(Date.parse(c.updated_at)) &&
      c.campaign && businessKeys.every(k => typeof c.campaign[k] === 'string') &&
      c.texts && textKeys.every(k => typeof c.texts[k] === 'string' && c.texts[k].length <= 10000) &&
      ['headline_1','headline_2','headline_3'].includes(c.selected_headline) &&
      typeof c.promotion_confirmed === 'boolean' && typeof c.promotion_terms === 'string' &&
      c.visual && templates.some(t => t[0] === c.visual.template) &&
      ['cuadrado','vertical'].includes(c.visual.format) &&
      typeof c.visual.headline === 'string' && typeof c.visual.subtext === 'string' &&
      Object.keys(colors).every(k => color(c.visual[k])) &&
      (c.visual.image === undefined || c.visual.image === '' ||
        (typeof c.visual.image === 'string' && c.visual.image.length <= 1500000 && /^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(c.visual.image)));
  }
  function read() {
    const raw = localStorage.getItem(KEY);
    if (raw === null) return [];
    let data;
    try { data = JSON.parse(raw); } catch (_) { throw new Error('El historial contiene JSON dañado. No lo sobrescribiremos ni eliminaremos.'); }
    if (!data || data.version !== 1 || !Array.isArray(data.campaigns) || !data.campaigns.every(valid) || new Set(data.campaigns.map(c=>c.id)).size !== data.campaigns.length)
      throw new Error('El historial tiene un formato incompatible o datos dañados. Se conserva sin cambios.');
    return data.campaigns;
  }
  function write(items) {
    if (new Set(items.map(c=>c.id)).size !== items.length) throw new Error('IDs duplicados. No se modificó el historial.');
    if (!items.every(valid)) throw new Error('Los datos no son válidos. No se modificó el historial.');
    localStorage.setItem(KEY, JSON.stringify({version:1,campaigns:items}));
  }
  function message(e) {
    if (e && (e.name === 'QuotaExceededError' || e.code === 22)) return 'No hay espacio en el navegador. Reduce o quita la imagen, o elimina una campaña que ya no necesites. No se guardaron los cambios.';
    if (e && e.name === 'SecurityError') return 'El navegador bloquea el almacenamiento local. Habilítalo para este sitio; tus cambios siguen aquí, pero no se guardaron.';
    return (e && e.message) || 'No se pudo acceder al almacenamiento. Tus cambios se conservan en esta pantalla.';
  }
  const buttonClass = 'inline-flex items-center justify-center gap-2 rounded-xl border border-[#242668]/20 bg-white px-4 py-3 text-sm font-medium text-[#242668] hover:bg-[#242668]/5 focus-visible:outline-2 focus-visible:outline-[#242668] disabled:opacity-50';
  const controlClass = 'w-full rounded-xl border border-[#242668]/20 bg-white px-4 py-3 text-sm text-[#202126] focus-visible:outline-2 focus-visible:outline-[#242668]';
  function el(tag, text, cls) {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  }
  function status(text, error=false) {
    const node = document.getElementById('browser-status');
    if (node) { node.textContent = text; node.className = error ? 'my-4 text-sm leading-6 text-red-800' : 'my-4 text-sm leading-6 text-[#242668]'; node.setAttribute('role',error?'alert':'status'); }
  }
  function btn(text, handler) {
    const b = el('button',text,buttonClass); b.type='button'; b.addEventListener('click',handler); return b;
  }
  function mark() { dirty = true; status('Cambios sin guardar en el historial.'); }
  function field(parent, key, title, multiline=false) {
    const wrapper = el('div',undefined,'mb-5');
    const label = el('label', title,'mb-2 block text-sm font-semibold text-[#242668]'); label.htmlFor='visual-'+key;
    const input = el(multiline?'textarea':'input',undefined,controlClass); input.id='visual-'+key;
    input.value=current.visual[key]; input.maxLength=key==='headline'?240:800;
    if (multiline) input.rows=4;
    input.addEventListener('input',()=>{current.visual[key]=input.value; mark(); preview();});
    wrapper.append(label,input); parent.append(wrapper);
  }
  function choice(parent,title,options,key) {
    const group=el('fieldset',undefined,'mb-6'); group.append(el('legend',title,'mb-3 text-sm font-semibold text-[#242668]'));
    const row=el('div',undefined,'flex flex-wrap gap-2');
    options.forEach(([value,label])=>{
      const b=btn(label,()=>{current.visual[key]=value; mark(); Array.from(row.children).forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.value===value))); preview();});
      b.dataset.value=value; b.setAttribute('aria-pressed',String(current.visual[key]===value));
      b.className=buttonClass+' aria-pressed:bg-[#242668] aria-pressed:text-white'; row.append(b);
    }); group.append(row); parent.append(group);
  }
  function loadImage(src) {
    return new Promise((resolve,reject)=>{ const i=new Image(); i.onload=()=>resolve(i); i.onerror=()=>reject(new Error('No se pudo leer la imagen. Prueba con otro JPG, PNG o WebP.')); i.src=src; });
  }
  function cover(ctx,img,x,y,w,h) {
    const scale=Math.max(w/img.width,h/img.height), sw=w/scale,sh=h/scale;
    ctx.drawImage(img,(img.width-sw)/2,(img.height-sh)/2,sw,sh,x,y,w,h);
  }
  function lines(ctx,text,width) {
    const result=[];
    String(text).split('\n').forEach(p=>{
      let line='';
      p.split(/\s+/).forEach(word=>{
        if (ctx.measureText(word).width>width) {
          if(line){result.push(line);line='';}
          for (const char of word) { if(ctx.measureText(line+char).width>width){result.push(line);line='';} line+=char; }
        } else if (ctx.measureText(line ? line+' '+word : word).width>width) { result.push(line);line=word; }
        else line=line?line+' '+word:word;
      }); result.push(line);
    }); return result;
  }
  function textBlock(ctx,text,x,y,w,h,start,weight,ink,center=false) {
    let size=start, parts;
    do {ctx.font=weight+' '+size+'px Inter, sans-serif';parts=lines(ctx,text,w);if(parts.length*size*1.24<=h)break;size-=2;}while(size>=18);
    if(parts.length*size*1.24>h) throw new Error('El texto es demasiado largo para esta plantilla. Acorta el titular o el texto secundario; no se descargará un diseño recortado.');
    ctx.fillStyle=ink;ctx.textAlign=center?'center':'left';ctx.textBaseline='top';
    parts.forEach((line,i)=>ctx.fillText(line,center?x+w/2:x,y+i*size*1.24));
    ctx.textAlign='left';
  }
  async function render(canvas,c) {
    await document.fonts.ready;
    const v=c.visual, w=1080,h=v.format==='vertical'?1920:1080;
    canvas.width=w; canvas.height=h;
    const ctx=canvas.getContext('2d'); if(!ctx)throw new Error('Este navegador no permite crear imágenes Canvas.');
    ctx.fillStyle=v.background;ctx.fillRect(0,0,w,h);
    const img=v.image?await loadImage(v.image):null;
    let top=150, bottom=h-100, center=false;
    if(v.template==='split') {
      const photoH=Math.round(h*.43);
      if(img)cover(ctx,img,0,0,w,photoH);
      else {ctx.fillStyle=v.accent;ctx.fillRect(0,0,w,photoH);ctx.fillStyle=v.background;ctx.beginPath();ctx.arc(820,photoH*.5,photoH*.3,0,Math.PI*2);ctx.fill();}
      ctx.fillStyle=v.accent;ctx.fillRect(72,photoH+65,100,12); top=photoH+125;
    } else if(v.template==='frame') {
      ctx.strokeStyle=v.accent;ctx.lineWidth=18;ctx.strokeRect(35,35,w-70,h-70);center=true;
      if(img) {cover(ctx,img,90,100,900,h*.3); top=100+h*.3+60;}
      else {ctx.strokeStyle=v.accent;ctx.lineWidth=6;ctx.beginPath();ctx.arc(w/2,130,40,0,Math.PI*2);ctx.stroke();top=240;}
      bottom=h-135;
    } else {
      ctx.fillStyle=v.accent;ctx.beginPath();ctx.arc(1010,45,145,0,Math.PI*2);ctx.fill();
      if(img){const ph=h*.33;cover(ctx,img,72,h-ph-72,936,ph);bottom=h-ph-120;}
      else {ctx.fillStyle=v.accent;ctx.fillRect(72,h-115,936,12);}
    }
    textBlock(ctx,c.campaign.nombre_negocio,72,65,800,60,30,'600',v.foreground);
    const available=bottom-top;
    textBlock(ctx,v.headline,72,top,936,available*.57,88,'700',v.foreground,center);
    textBlock(ctx,v.subtext,72,top+available*.62,936,available*.38,38,'400',v.foreground,center);
    return canvas;
  }
  async function preview() {
    const n=++epoch, canvas=document.getElementById('design-preview'); if(!canvas||!current)return;
    try {
      const temp=document.createElement('canvas');await render(temp,clone(current));
      if(n!==epoch||!canvas.isConnected)return;
      canvas.width=temp.width;canvas.height=temp.height;canvas.getContext('2d').drawImage(temp,0,0);
      canvas.setAttribute('aria-label','Vista previa: '+current.visual.headline);
      const d=document.getElementById('design-dimensions'); if(d)d.textContent=temp.width+' × '+temp.height+' px · PNG';
    }catch(e){if(n===epoch)status(message(e),true);}
  }
  async function pickImage(file) {
    if(!file)return;
    imageBusy=true;status('Procesando imagen en este navegador…');
    try {
      if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size>20*1024*1024)throw new Error('Elige JPG, PNG o WebP de hasta 20 MB. No se aceptan SVG ni archivos animados.');
      const raw=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=()=>reject(new Error('No se pudo leer el archivo.'));r.readAsDataURL(file);});
      const img=await loadImage(raw);
      if(img.width*img.height>50000000)throw new Error('La imagen es demasiado grande. Redúcela antes de seleccionarla.');
      const c=document.createElement('canvas'),scale=Math.min(1,1440/Math.max(img.width,img.height));
      c.width=Math.max(1,Math.round(img.width*scale));c.height=Math.max(1,Math.round(img.height*scale));
      const ctx=c.getContext('2d');ctx.fillStyle='#FFFFFF';ctx.fillRect(0,0,c.width,c.height);ctx.drawImage(img,0,0,c.width,c.height);
      let quality=.85, data=c.toDataURL('image/jpeg',quality);
      while(data.length>1000000&&quality>.35){quality-=.1;data=c.toDataURL('image/jpeg',quality);}
      if(data.length>1500000)throw new Error('No se pudo comprimir suficientemente la imagen. Selecciona una más pequeña.');
      current.visual.image=data;mark();await preview();status('Imagen lista, redimensionada y comprimida localmente. Guarda para conservarla.');
    }catch(e){status(message(e),true);}finally{imageBusy=false;}
  }
  async function download() {
    try {
      if(imageBusy)throw new Error('Espera a que termine el procesamiento de la imagen.');
      const c=document.createElement('canvas');await render(c,clone(current));
      const blob=await new Promise((resolve,reject)=>c.toBlob(b=>b?resolve(b):reject(new Error('No se pudo crear el PNG.')),'image/png'));
      const url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download='impulso-'+c.width+'x'+c.height+'.png';
      document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
      status('PNG generado. Se solicitó la descarga al navegador; revisa tu carpeta de descargas. No podemos confirmar que lo haya guardado.');
    }catch(e){status(message(e),true);}
  }
  function save() {
    try {
      if(imageBusy)throw new Error('Espera a que termine la imagen antes de guardar.');
      const items=read(),c=clone(current),index=items.findIndex(x=>x.id===c.id);
      if(index>=0&&items[index].updated_at!==c.updated_at)throw new Error('Esta campaña cambió en otra pestaña. No sobrescribimos esa versión. Guarda una copia o vuelve a abrirla desde el historial.');
      c.updated_at=new Date().toISOString();
      if(index>=0){c.created_at=items[index].created_at;items[index]=c;}else items.push(c);
      write(items);current=c;dirty=false;status(index>=0?'Campaña actualizada en este navegador.':'Campaña guardada en este navegador.');
      const label=document.getElementById('save-campaign');if(label)label.textContent='Actualizar campaña';
    }catch(e){status(message(e),true);}
  }
  function receive(c) {
    const image=current&&current.id===c.id?current.visual.image:'';
    current=clone(c);
    if(!current.id)current.id=crypto.randomUUID();
    if(!current.created_at)current.created_at=new Date().toISOString();
    if(!current.updated_at)current.updated_at=current.created_at;
    current.visual={...colors,template:'editorial',format:c.campaign.formato||'cuadrado',headline:'',subtext:'',...c.visual,image:image||''};
    if(current.visual.initialized !== 'true') {
      current.visual.headline=c.texts[c.selected_headline]||'';
      current.visual.subtext=c.texts.description||'';
      current.visual.initialized='true';
    }
    dirty=true;
  }
  async function waitForRoot(id) {
    for(let attempt=0;attempt<100;attempt++) {
      const root=document.getElementById(id);
      if(root)return root;
      await new Promise(resolve=>setTimeout(resolve,50));
    }
    const root=document.getElementById(id);
    if(root)return root;
    const error=new Error(id==='history-root'?'No se pudo preparar el historial. Pulsa Actualizar historial o recarga la página.':'No se pudo preparar el diseñador. Vuelve a intentar o recarga la página.');
    status(error.message,true);
    throw error;
  }
  async function designer(c) {
    const root=document.getElementById('designer-root') || await waitForRoot('designer-root');
    if(!current||current.id!==c.id)receive(c);
    else {const image=current.visual.image;current={...clone(c),visual:{...clone(c.visual),image}};}
    if(current.visual.initialized !== 'true') {
      current.visual.headline=current.texts[current.selected_headline]||'';
      current.visual.subtext=current.texts.description||'';
      current.visual.initialized='true';
    }
    root.replaceChildren();
    if(!current.campaign.nombre_negocio||!current.texts.headline_1) {
      root.append(el('p','No hay una campaña en esta sesión. Abre una guardada en el historial o crea una nueva.','text-sm leading-6 text-gray-600'));
      const link=el('a','Abrir historial',buttonClass);link.href='/historial';
      const create=el('a','Crear una campaña',buttonClass);create.href='/crear?nueva=1';
      root.append(link,create);return JSON.stringify({ok:true});
    }
    const controls=el('section',undefined,'rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-7');
    controls.append(el('h2','Tu composición','mb-5 text-xl font-semibold text-[#242668]'));
    choice(controls,'Plantilla gráfica',templates,'template');
    controls.append(el('p',templates.map(t=>t[1]+': '+t[2]).join(' '),'mb-6 text-xs leading-6 text-gray-600'));
    choice(controls,'Formato',[['cuadrado','Cuadrado · 1080 × 1080'],['vertical','Vertical · 1080 × 1920']],'format');
    field(controls,'headline','Titular del diseño',true);field(controls,'subtext','Texto secundario del diseño',true);
    controls.append(el('p','Estos textos solo cambian el diseño, no tus textos de publicación.','mb-5 text-xs text-gray-600'));
    const colorRow=el('div',undefined,'grid grid-cols-1 gap-3 sm:grid-cols-3');
    [['background','Fondo'],['foreground','Texto'],['accent','Acento']].forEach(([k,title])=>{
      const box=el('div'),label=el('label',title,'mb-2 block text-sm font-medium text-[#242668]');label.htmlFor='color-'+k;
      const i=el('input',undefined,controlClass);i.id='color-'+k;i.value=current.visual[k];i.maxLength=7;i.placeholder='#242668';
      i.addEventListener('input',()=>{const ok=color(i.value);i.setAttribute('aria-invalid',String(!ok));if(ok){current.visual[k]=i.value;mark();preview();}else status('Usa un color hexadecimal de seis dígitos, por ejemplo #242668. El color anterior se conserva.',true);});
      box.append(label,i);colorRow.append(box);
    });controls.append(colorRow,el('p','Usa #RRGGBB. Revisa que el texto contraste bien con el fondo.','my-3 text-xs text-gray-600'));
    const fileLabel=el('label','Imagen propia · opcional','mt-6 mb-2 block text-sm font-semibold text-[#242668]');fileLabel.htmlFor='local-image';
    const input=el('input',undefined,controlClass);input.type='file';input.id='local-image';input.accept='image/jpeg,image/png,image/webp';input.addEventListener('change',()=>pickImage(input.files[0]));
    controls.append(fileLabel,input,el('p','JPG, PNG o WebP, hasta 20 MB. Se comprime a un máximo de 1440 px y se recorta al centro. La imagen nunca se envía al servidor.','my-3 text-xs leading-5 text-gray-600'),btn('Quitar imagen',()=>{if(imageBusy){status('Espera a que termine la imagen.',true);return;}current.visual.image='';input.value='';mark();preview();}));
    const panel=el('section',undefined,'flex min-w-0 flex-col items-center rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-7');
    panel.append(el('h2','Vista previa','mb-4 w-full text-xl font-semibold text-[#242668]'));
    const canvas=el('canvas',undefined,'h-auto w-full max-w-[440px] bg-[#F8F7F2]');canvas.id='design-preview';canvas.setAttribute('role','img');
    const dim=el('p',undefined,'my-4 text-xs text-gray-600');dim.id='design-dimensions';
    panel.append(canvas,dim,el('p','La vista previa y el PNG utilizan la misma composición Canvas. No son imágenes creadas por IA.','mb-5 text-xs leading-6 text-gray-600'));
    const actions=el('div',undefined,'flex w-full flex-wrap gap-2');
    const saveButton=btn('Guardar / actualizar campaña',save);saveButton.id='save-campaign';
    actions.append(btn('Descargar PNG',download),saveButton,btn('Guardar como copia',()=>{try {if(imageBusy)throw new Error('Espera a que termine la imagen.');const copied=clone(current);copied.id=crypto.randomUUID();copied.created_at=copied.updated_at=new Date().toISOString();const items=read();items.push(copied);write(items);current=copied;dirty=false;status('Copia guardada con nuevo ID y fecha. Ahora editas la copia.');}catch(e){status(message(e),true);}}));
    panel.append(actions);root.append(controls,panel);preview();
    return JSON.stringify({ok:true});
  }
  function date(value){return new Date(value).toLocaleString('es',{dateStyle:'medium',timeStyle:'short'});}
  async function history() {
    const root=document.getElementById('history-root') || await waitForRoot('history-root');
    root.replaceChildren();status('Leyendo el historial de este navegador…');
    try {
      const items=read().sort((a,b)=>Date.parse(b.updated_at)-Date.parse(a.updated_at));
      status(items.length+' campañas · solo en este navegador, sin sincronización.');
      if(!items.length){root.append(el('p','Todavía no hay campañas guardadas. Crea un diseño y pulsa Guardar campaña.','col-span-full rounded-2xl border border-[#242668]/10 bg-white p-8 text-sm leading-6 text-gray-600'));return JSON.stringify({ok:true});}
      items.forEach(c=>{
        const card=el('article',undefined,'flex min-w-0 flex-col rounded-2xl border border-[#242668]/10 bg-white p-5');
        const canvas=el('canvas',undefined,'mb-5 h-auto w-full bg-[#F8F7F2]');canvas.setAttribute('role','img');canvas.setAttribute('aria-label','Diseño de '+c.campaign.nombre_negocio);
        const thumb=document.createElement('canvas');render(thumb,c).then(()=>{canvas.width=270;canvas.height=270*thumb.height/thumb.width;canvas.getContext('2d').drawImage(thumb,0,0,canvas.width,canvas.height);}).catch(()=>{canvas.remove();card.prepend(el('p','Vista previa no disponible; tus textos se conservan.','text-xs text-red-800'));});
        card.append(canvas,el('h2',c.campaign.nombre_negocio,'text-lg font-semibold text-[#242668]'),el('p',c.visual.headline,'mt-2 break-words text-sm text-[#202126]'),el('p','Creada: '+date(c.created_at),'mt-4 text-xs text-gray-600'),el('p','Actualizada: '+date(c.updated_at),'mt-2 text-xs text-gray-600'));
        const row=el('div',undefined,'mt-5 flex flex-wrap gap-2');
        row.append(btn('Abrir',()=>{if(dirty&&!window.confirm('Hay cambios sin guardar en el editor. ¿Descartarlos y abrir esta campaña?'))return;pendingOpen=clone(c);dirty=false;document.getElementById('restore-history-campaign').click();}),btn('Duplicar',()=>{try{const latest=read(),original=latest.find(x=>x.id===c.id);if(!original)throw new Error('La campaña ya no existe. Actualiza el historial.');const copy=clone(original);copy.id=crypto.randomUUID();copy.created_at=copy.updated_at=new Date().toISOString();latest.push(copy);write(latest);history().then(()=>status('Copia guardada con nuevo ID y fechas.'));}catch(e){status(message(e),true);}}));
        const confirm=el('div',undefined,'mt-4 rounded-xl border border-red-200 bg-red-50 p-4');confirm.hidden=true;
        confirm.append(el('p','¿Eliminar «'+c.campaign.nombre_negocio+'» de este navegador? No se puede deshacer.','mb-3 text-sm text-red-800'),btn('Cancelar',()=>{confirm.hidden=true;del.focus();}),btn('Sí, eliminar',()=>{try{const latest=read(),found=latest.find(x=>x.id===c.id);if(found&&found.updated_at!==c.updated_at)throw new Error('Esta campaña cambió. Actualiza el historial antes de eliminar.');write(latest.filter(x=>x.id!==c.id));history().then(()=>status('Campaña eliminada de este navegador.'));}catch(e){status(message(e),true);}}));
        const del=btn('Eliminar',()=>{confirm.hidden=false;confirm.querySelector('button').focus();});row.append(del);card.append(row,confirm);root.append(card);
      });
    }catch(e){status(message(e),true);root.append(btn('Volver a intentar',history));}
    return JSON.stringify({ok:true});
  }
  function captureContent() {
    const result={texts:{},pending_terms:'',pending_approved:false};
    textKeys.forEach(k=>{const node=document.getElementById(k);if(node)result.texts[k]=node.value;});
    const terms=document.getElementById('promotion-terms'),approved=document.getElementById('promotion-approved');
    if(terms)result.pending_terms=terms.value;if(approved)result.pending_approved=approved.checked;
    return JSON.stringify(result);
  }
  function withoutImage(c) {const data=clone(c);delete data.visual.image;return JSON.stringify(data);}
  function resolve(c) {
    if(current&&current.id===c.id) {const image=current.visual.image,created=current.created_at,updated=current.updated_at;current={...clone(c),created_at:created,updated_at:updated,visual:{...clone(c.visual),image}};return withoutImage(current);}
    if(current&&(!c.id||!c.content_ready))return withoutImage(current);
    if(c.id) {try {const saved=read().find(x=>x.id===c.id);if(saved){saved.campaign=c.campaign;saved.texts=c.texts;saved.promotion_confirmed=c.promotion_confirmed;saved.promotion_terms=c.promotion_terms;saved.selected_headline=c.selected_headline;current=saved;return withoutImage(saved);}}catch(e){status(message(e),true);}}
    return 'null';
  }
  function editorData() {if(imageBusy)throw new Error('Espera a que termine la imagen.');const c=clone(current);delete c.visual.image;return JSON.stringify(c);}
  function consumeOpen() {if(!pendingOpen)throw new Error('No se seleccionó una campaña.');formDraft=null;formStarted=false;current=pendingOpen;pendingOpen=null;const c=clone(current);delete c.visual.image;return JSON.stringify(c);}
  document.addEventListener('click',e=>{
    const link=e.target.closest('a[href]');
    if(link && dirty && link.getAttribute('href').includes('nueva=1')) {
      if(!window.confirm('Hay cambios sin guardar. ¿Descartarlos y crear una nueva campaña?')) {e.preventDefault();e.stopPropagation();}
      else {current=null;dirty=false;}
    }
  },true);
  window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
  window.ImpulsoBrowser={designer,history,receive,resolve,editorData,consumeOpen,captureContent,valid,lines,read,write,preferences,prepareForm};
})();
"""
