const cacheName = 'saftpwa';
 
const assets = [
//	'/static/js/main.js',
// bør kanskje også legge til main.py, analyse.py osv her?
	'/static/pyodide/pyscript.css',
	'/static/pyodide/pyscript.min.js',
	'/static/pyodide/pyodide.js',
	'/static/pyodide/pyodide_py.tar',
	'/static/pyodide/pyodide.js.map',
	'/static/pyodide/pyodide.asm.js',
	'/static/pyodide/pyodide.asm.data',
	'/static/pyodide/repodata.json',
	'/static/pyodide/pyodide.asm.wasm',
	'/static/pyodide/pyparsing-3.0.9-py3-none-any.whl',
	'/static/pyodide/micropip-0.1-py3-none-any.whl',
	'/static/pyodide/packaging-21.3-py3-none-any.whl',
	'/static/pyodide/distutils.tar', 
	'/static/pyodide/matplotlib-3.5.2-cp310-cp310-emscripten_3_1_14_wasm32.whl',
	'/static/pyodide/kiwisolver-1.4.3-cp310-cp310-emscripten_3_1_14_wasm32.whl',
	'/static/pyodide/numpy-1.22.4-cp310-cp310-emscripten_3_1_14_wasm32.whl',
	'/static/pyodide/fonttools-4.33.3-py3-none-any.whl',
	'/static/pyodide/six-1.16.0-py2.py3-none-any.whl',
	'/static/pyodide/cycler-0.11.0-py3-none-any.whl',
	 '/static/pyodide/PIL-9.1.1-cp310-cp310-emscripten_3_1_14_wasm32.whl',
	 '/static/pyodide/pytz-2022.1-py2.py3-none-any.whl',
	 '/static/pyodide/pandas-1.4.2-cp310-cp310-emscripten_3_1_14_wasm32.whl',
	 '/static/pyodide/setuptools-62.6.0-py3-none-any.whl',
	 '/static/pyodide/python_dateutil-2.8.2-py2.py3-none-any.whl',
];
 
self.addEventListener('install', e => {
	console.log('Service Worker: Installed');
	e.waitUntil(
		caches.open(cacheName).then((cache) => {
			cache.addAll(assets);
		})
	);
});
 
// self.addEventListener('activate', e => {
// 	console.log('Service Worker: Activated');
// });
 
self.addEventListener('fetch', e => {
	e.respondWith(
		fetch(e.request)
		.then(res => {
			const resClone = res.clone();
			caches.open(cacheName).then(cache => {
				cache.put(e.request, resClone);
			});
			return res;
		})
		.catch(err => caches.match(e.request).then(res => res))
	);
});