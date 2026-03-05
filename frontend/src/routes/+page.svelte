<script>
    import { onMount } from 'svelte';

    // Gestión de Estado (Reactividad)
    let funcion = '';
    let x0 = 0;
    let tolerancia = 0.0001;
    let maxIteraciones = 50;

    let resultados = [];
    let raiz = null;
    let cargando = false;
    let mensajeError = '';
    let mensajeExito = '';

    let funcionInput;

    // Funciones del teclado virtual matemático
    function insertText(text) {
        if (funcionInput) {
            const start = funcionInput.selectionStart;
            const end = funcionInput.selectionEnd;
            funcion = funcion.substring(0, start) + text + funcion.substring(end);
            
            // Re-enfocar y mover el cursor después del texto insertado
            setTimeout(() => {
                funcionInput.selectionStart = funcionInput.selectionEnd = start + text.length;
                funcionInput.focus();
            }, 0);
        } else {
            funcion += text;
        }
    }

    function backspace() {
        if (funcionInput && funcionInput.selectionStart > 0) {
            const start = funcionInput.selectionStart;
            const end = funcionInput.selectionEnd;
            
            if (start === end) {
                // Borrar un caracter hacia atrás
                funcion = funcion.substring(0, start - 1) + funcion.substring(end);
                setTimeout(() => {
                    funcionInput.selectionStart = funcionInput.selectionEnd = start - 1;
                    funcionInput.focus();
                }, 0);
            } else {
                // Borrar selección actual
                funcion = funcion.substring(0, start) + funcion.substring(end);
                setTimeout(() => {
                    funcionInput.selectionStart = funcionInput.selectionEnd = start;
                    funcionInput.focus();
                }, 0);
            }
        } else if (!funcionInput) {
            funcion = funcion.slice(0, -1);
        }
    }

    function clearFunction() {
        funcion = '';
        if (funcionInput) funcionInput.focus();
    }

    // Conexión con la API
    async function calcularRaiz() {
        if (!funcion) {
            mensajeError = 'Por favor, ingresa una función.';
            return;
        }

        cargando = true;
        mensajeError = '';
        mensajeExito = '';
        resultados = [];
        raiz = null;

        try {
            const res = await fetch('http://localhost:8000/api/calcular-raiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    funcion: funcion,
                    x0: parseFloat(x0),
                    tolerancia: parseFloat(tolerancia),
                    max_iteraciones: parseInt(maxIteraciones)
                })
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Error al calcular la raíz');
            }

            if (!data.exito) {
                mensajeError = data.mensaje;
            } else {
                mensajeExito = data.mensaje;
            }

            resultados = data.iteraciones || [];
            raiz = data.raiz !== undefined ? data.raiz : null;

        } catch (error) {
            mensajeError = error.message;
        } finally {
            cargando = false;
        }
    }
</script>

<div class="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
    <div class="max-w-5xl mx-auto">
        
        <div class="text-center mb-10">
            <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight sm:text-4xl">
                Calculadora Newton-Raphson
            </h1>
            <p class="mt-4 text-lg text-slate-600">
                Encuentra raíces de funciones matemáticas usando el método numérico de Newton-Raphson.
            </p>
        </div>

        <div class="bg-white shadow-sm ring-1 ring-slate-200 sm:rounded-xl mb-8">
            <div class="px-4 py-6 sm:p-8">
                <!-- Formulario de Entrada -->
                <form on:submit|preventDefault={calcularRaiz} class="space-y-6">
                    <div class="grid grid-cols-1 gap-y-6 gap-x-6 sm:grid-cols-2 lg:grid-cols-3">
                        <div class="sm:col-span-2 lg:col-span-3">
                            <label for="funcion" class="block text-sm font-semibold text-slate-700">Función f(x)</label>
                            <div class="mt-2">
                                <input 
                                    bind:this={funcionInput}
                                    type="text" 
                                    id="funcion" 
                                    bind:value={funcion} 
                                    placeholder="ej. x^2 - 4 o sin(x) - x/2" 
                                    class="block w-full rounded-md border-0 py-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 text-lg sm:text-2xl font-mono px-4" 
                                    required
                                >
                            </div>
                        </div>

                        <div>
                            <label for="x0" class="block text-sm font-semibold text-slate-700">Punto inicial (x₀)</label>
                            <div class="mt-2">
                                <input 
                                    type="number" 
                                    step="any" 
                                    id="x0" 
                                    bind:value={x0} 
                                    class="block w-full rounded-md border-0 py-2 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3" 
                                    required
                                >
                            </div>
                        </div>

                        <div>
                            <label for="tolerancia" class="block text-sm font-semibold text-slate-700">Tolerancia</label>
                            <div class="mt-2">
                                <input 
                                    type="number" 
                                    step="any" 
                                    id="tolerancia" 
                                    bind:value={tolerancia} 
                                    class="block w-full rounded-md border-0 py-2 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3" 
                                    required
                                >
                            </div>
                        </div>

                        <div>
                            <label for="maxIteraciones" class="block text-sm font-semibold text-slate-700">Máx. Iteraciones</label>
                            <div class="mt-2">
                                <input 
                                    type="number" 
                                    id="maxIteraciones" 
                                    bind:value={maxIteraciones} 
                                    class="block w-full rounded-md border-0 py-2 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3" 
                                    required
                                >
                            </div>
                        </div>
                    </div>

                    <!-- Teclado Matemático Virtual -->
                    <div class="sm:col-span-2 lg:col-span-3 mt-8 bg-slate-100 p-4 sm:p-6 rounded-xl shadow-inner border border-slate-200">
                        <div class="text-xs font-semibold text-slate-500 mb-3 uppercase tracking-wider">Teclado Matemático</div>
                        
                        <div class="grid grid-cols-4 sm:grid-cols-8 gap-2 mb-2">
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('sin(')}>sin</button>
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('cos(')}>cos</button>
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('tan(')}>tan</button>
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('sqrt(')}>√</button>
                            
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('exp(')}>exp</button>
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('log(')}>ln</button>
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('pi')}>π</button>
                            <button type="button" class="bg-white hover:bg-blue-50 text-blue-700 font-semibold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-sm font-mono" on:click={() => insertText('E')}>e</button>
                        </div>

                        <div class="grid grid-cols-4 sm:grid-cols-8 gap-2">
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('7')}>7</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('8')}>8</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('9')}>9</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText(' / ')}>÷</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('^')}>^</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('(')}>(</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText(')')}>)</button>
                            <button type="button" class="bg-red-50 hover:bg-red-100 text-red-600 font-bold py-2 px-3 border border-red-200 rounded shadow-sm transition-colors text-sm font-mono flex items-center justify-center" on:click={backspace}>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9.75L14.25 12m0 0l2.25 2.25M14.25 12l2.25-2.25M14.25 12L12 14.25m-2.58 4.92l-6.375-6.375a1.125 1.125 0 010-1.59L9.42 4.83c.211-.211.498-.33.796-.33H19.5a2.25 2.25 0 012.25 2.25v10.5a2.25 2.25 0 01-2.25 2.25h-9.284c-.298 0-.585-.119-.796-.33z" /></svg>
                            </button>
                            
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('4')}>4</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('5')}>5</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('6')}>6</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText(' * ')}>×</button>
                            <button type="button" class="bg-amber-100 hover:bg-amber-200 text-amber-900 font-bold py-2 px-3 border border-amber-300 rounded shadow-sm transition-colors text-xl font-mono col-span-2 row-span-2 flex items-center justify-center" on:click={() => insertText('x')}>x</button>
                            <button type="button" class="bg-red-50 hover:bg-red-100 text-red-700 font-bold py-2 px-3 border border-red-200 rounded shadow-sm transition-colors text-sm font-mono col-span-2" on:click={clearFunction}>AC</button>
                            
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('1')}>1</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('2')}>2</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('3')}>3</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText(' - ')}>−</button>
                            
                            <!-- Placeholder to keep grid aligned since "x" takes 2 rows -->
                            <div class="col-span-2 hidden sm:block"></div> 

                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono col-span-2" on:click={() => insertText('0')}>0</button>
                            <button type="button" class="bg-white hover:bg-slate-50 text-slate-800 font-bold py-2 px-3 border border-slate-300 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText('.')}>.</button>
                            <button type="button" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 border border-indigo-200 rounded shadow-sm transition-colors text-lg font-mono" on:click={() => insertText(' + ')}>+</button>
                        </div>
                    </div>

                    <div class="flex items-center justify-end pt-4">
                        <button 
                            type="submit" 
                            disabled={cargando} 
                            class="rounded-md bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            {cargando ? 'Calculando...' : 'Calcular Raíz'}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Alertas -->
        {#if mensajeError}
            <div class="rounded-md bg-red-50 p-4 mb-8 border border-red-200 shadow-sm">
                <div class="flex">
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-red-800">Se produjo un error</h3>
                        <div class="mt-2 text-sm text-red-700">
                            <p>{mensajeError}</p>
                        </div>
                    </div>
                </div>
            </div>
        {/if}

        {#if mensajeExito}
            <div class="rounded-md bg-green-50 p-4 mb-8 border border-green-200 shadow-sm">
                <div class="flex items-center">
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-green-800">Cálculo Exitoso</h3>
                        <div class="mt-2 text-sm text-green-700">
                            <p>
                                {mensajeExito} 
                                {#if raiz !== null}
                                    <span class="font-bold ml-1">Raíz aproximada: {raiz.toFixed(8)}</span>
                                {/if}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        {/if}

        <!-- Tabla de Resultados -->
        {#if resultados.length > 0}
            <div class="mt-8 flow-root">
                <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
                            <table class="min-w-full divide-y divide-slate-300">
                                <thead class="bg-slate-50">
                                    <tr>
                                        <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-slate-900 sm:pl-6">Iteración</th>
                                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">xᵢ</th>
                                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">f(xᵢ)</th>
                                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">f'(xᵢ)</th>
                                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Error Relativo</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-200 bg-white">
                                    {#each resultados as fila}
                                        <tr class="hover:bg-slate-50 transition-colors">
                                            <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-slate-900 sm:pl-6">
                                                {fila.paso}
                                            </td>
                                            <td class="whitespace-nowrap px-3 py-4 text-sm text-slate-500 font-mono">
                                                {fila.x_actual.toFixed(8)}
                                            </td>
                                            <td class="whitespace-nowrap px-3 py-4 text-sm text-slate-500 font-mono">
                                                {fila.f_x.toExponential(4)}
                                            </td>
                                            <td class="whitespace-nowrap px-3 py-4 text-sm text-slate-500 font-mono">
                                                {fila.f_derivada_x.toFixed(6)}
                                            </td>
                                            <td class="whitespace-nowrap px-3 py-4 text-sm text-slate-500 font-mono">
                                                {fila.error_relativo !== null ? fila.error_relativo.toExponential(4) : '-'}
                                            </td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        {/if}

    </div>
</div>