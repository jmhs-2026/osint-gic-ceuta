const V='osint-v5';
const SHELL=['./','index.html','manifest.webmanifest?v=1','icon-192.png?v=1','icon-512.png?v=1','logo.webp?v=1','t-inmigracion.webp?v=1','t-amenazas.webp?v=1','t-paloma.webp?v=1','t-ordenpublico.webp?v=1'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url); if(e.request.method!=='GET'||u.origin!==location.origin)return;
  if(u.pathname.endsWith('.json')||u.pathname.endsWith('data.json')||u.pathname.endsWith('/')||u.pathname.endsWith('index.html')){
    e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request)));
  }else{
    e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));
  }
});

self.addEventListener('push',e=>{
  let d={title:'OSINT',body:'Nuevo barrido',tag:'osint'};try{d=Object.assign(d,e.data.json())}catch(x){}
  e.waitUntil(self.registration.showNotification(d.title,{body:d.body,tag:d.tag,icon:'icon-192.png',badge:'icon-192.png',renotify:true}));
});
self.addEventListener('notificationclick',e=>{
  e.notification.close();
  e.waitUntil(clients.matchAll({type:'window',includeUncontrolled:true}).then(l=>{for(const c of l){if('focus' in c)return c.focus()}return clients.openWindow('./')}));
});
