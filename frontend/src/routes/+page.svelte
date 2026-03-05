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
                funcion = funcion.substring(0, start - 1) + funcion.substring(end);
                setTimeout(() => {
                    funcionInput.selectionStart = funcionInput.selectionEnd = start - 1;
                    funcionInput.focus();
                }, 0);
            } else {
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
            mensajeError = 'Por favor, ingresa una función!!!';
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
                throw new Error(data.detail || 'Error Fatal al calcular!');
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

<style>
    /* Retro 2000s Styles */
    :global(body) {
        background-color: #000080;
        background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAABZJREFUeNpi2P//vwMTAwMDEwMD1AEgwAEAHY4DwR55rD8AAAAASUVORK5CYII=');
        color: #FFFF00;
        font-family: "Comic Sans MS", "Comic Sans", cursive, sans-serif;
    }
    
    .retro-container {
        /*max-w-4xl;*/
        margin: 0 auto;
        padding: 20px;
        background-color: #C0C0C0;
        border: 4px outset #FFFFFF;
        color: #000000;
    }

    .retro-header {
        text-align: center;
        border: 4px inset #FFFFFF;
        background: #000080;
        color: #FFFF00;
        padding: 10px;
        margin-bottom: 20px;
    }

    h1 {
        font-family: "Times New Roman", Times, serif;
        text-shadow: 2px 2px #FF0000;
        font-size: 36px;
        margin: 0;
    }

    .marquee-text {
        font-size: 16px;
        font-weight: bold;
        color: #00FF00;
        background-color: #000000;
        padding: 5px;
        border: 2px solid #00FF00;
    }

    .retro-panel {
        border: 4px inset #FFFFFF;
        padding: 15px;
        background: #D4D0C8;
        margin-bottom: 20px;
    }

    .retro-input {
        border: 2px inset #FFFFFF;
        background: #FFFFFF;
        color: #000000;
        padding: 5px;
        font-family: monospace;
        font-size: 16px;
    }

    .retro-button {
        background: #C0C0C0;
        border: 3px outset #FFFFFF;
        color: #000000;
        font-weight: bold;
        cursor: pointer;
        font-family: "Comic Sans MS", cursive;
        padding: 5px 10px;
    }
    
    .retro-button:active {
        border: 3px inset #FFFFFF;
        background: #A0A0A0;
    }

    .retro-button-red {
        background: #FF0000;
        color: #FFFFFF;
        border: 3px outset #FF8080;
    }

    .retro-button-red:active {
        border: 3px inset #FF8080;
    }

    .retro-button-blue {
        background: #0000FF;
        color: #FFFFFF;
        border: 3px outset #8080FF;
    }

    .retro-button-blue:active {
        border: 3px inset #8080FF;
    }

    .retro-table {
        width: 100%;
        border-collapse: collapse;
        border: 3px outset #FFFFFF;
        background: #FFFFFF;
    }

    .retro-table th, .retro-table td {
        border: 1px solid #808080;
        padding: 8px;
        text-align: left;
    }

    .retro-table th {
        background: #000080;
        color: #FFFFFF;
        font-family: "Times New Roman", Times, serif;
    }

    .retro-table tr:nth-child(even) {
        background: #E0E0E0;
    }

    .alert-error {
        background: #FF0000;
        color: #FFFF00;
        border: 4px outset #FF0000;
        padding: 10px;
        font-weight: bold;
        text-align: center;
        text-decoration: blink;
        margin-bottom: 20px;
    }

    .alert-success {
        background: #00FF00;
        color: #000000;
        border: 4px outset #00FF00;
        padding: 10px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    hr {
        border: 0;
        border-top: 2px groove #FFFFFF;
        margin: 20px 0;
    }
</style>

<div class="retro-container">
    <div class="retro-header">
        <h1>★★★ Calculadora Newton-Raphson ★★★</h1>
    </div>
    
    <marquee class="marquee-text" scrollamount="5">
        ¡Encuentra raíces de funciones matemáticas usando el método numérico de Newton-Raphson! ¡Totalmente GRATIS! ¡Diseñado para la Web 2.0!
    </marquee>

    <div class="retro-panel mt-4">
        <form on:submit|preventDefault={calcularRaiz}>
            <table width="100%" cellpadding="5">
                <tbody>
                    <tr>
                        <td colspan="3">
                            <label for="funcion"><b>Función f(x):</b></label><br>
                            <input 
                                bind:this={funcionInput}
                                type="text" 
                                id="funcion" 
                                bind:value={funcion} 
                                placeholder="Ej. x^2 - 4" 
                                class="retro-input"
                                style="width: 95%; font-size: 20px; padding: 10px; color: blue; font-weight: bold;"
                                required
                            >
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="x0"><b>Punto inicial (x₀):</b></label><br>
                            <input type="number" step="any" id="x0" bind:value={x0} class="retro-input" required>
                        </td>
                        <td>
                            <label for="tolerancia"><b>Tolerancia:</b></label><br>
                            <input type="number" step="any" id="tolerancia" bind:value={tolerancia} class="retro-input" required>
                        </td>
                        <td>
                            <label for="maxIteraciones"><b>Máx. Iteraciones:</b></label><br>
                            <input type="number" id="maxIteraciones" bind:value={maxIteraciones} class="retro-input" required>
                        </td>
                    </tr>
                </tbody>
            </table>

            <hr>
            
            <!-- Teclado Matemático Virtual Retro -->
            <div style="text-align: center;">
                <b>[ Teclado Matemático Virtual ]</b>
            </div>
            
            <table align="center" cellspacing="4" cellpadding="0" style="margin-top: 10px;">
                <tbody>
                    <tr>
                        <td><button type="button" class="retro-button" on:click={() => insertText('sin(')}>sin</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('cos(')}>cos</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('tan(')}>tan</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('sqrt(')}>√</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('exp(')}>exp</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('log(')}>ln</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('pi')}>π</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('E')}>e</button></td>
                    </tr>
                    <tr>
                        <td><button type="button" class="retro-button" on:click={() => insertText('7')}>7</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('8')}>8</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('9')}>9</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText(' / ')}>÷</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText('^')}>^</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText('(')}>(</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText(')')}>)</button></td>
                        <td><button type="button" class="retro-button retro-button-red" on:click={backspace}>⌫</button></td>
                    </tr>
                    <tr>
                        <td><button type="button" class="retro-button" on:click={() => insertText('4')}>4</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('5')}>5</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('6')}>6</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText(' * ')}>×</button></td>
                        <td colspan="2" rowspan="2"><button type="button" class="retro-button" style="width: 100%; height: 100%; font-size: 24px; color: #800000;" on:click={() => insertText('x')}>x</button></td>
                        <td colspan="2"><button type="button" class="retro-button retro-button-red" style="width: 100%;" on:click={clearFunction}>BORRAR TODO</button></td>
                    </tr>
                    <tr>
                        <td><button type="button" class="retro-button" on:click={() => insertText('1')}>1</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('2')}>2</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('3')}>3</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText(' - ')}>−</button></td>
                        <td colspan="2">&nbsp;</td>
                    </tr>
                    <tr>
                        <td colspan="2"><button type="button" class="retro-button" style="width: 100%;" on:click={() => insertText('0')}>0</button></td>
                        <td><button type="button" class="retro-button" on:click={() => insertText('.')}>.</button></td>
                        <td><button type="button" class="retro-button retro-button-blue" on:click={() => insertText(' + ')}>+</button></td>
                        <td colspan="4">&nbsp;</td>
                    </tr>
                </tbody>
            </table>

            <hr>
            
            <div style="text-align: center; margin-top: 15px;">
                <button 
                    type="submit" 
                    disabled={cargando} 
                    class="retro-button"
                    style="font-size: 20px; padding: 10px 30px; background: #008000; color: white;"
                >
                    {cargando ? 'CALCULANDO...' : '¡CALCULAR RAÍZ!'}
                </button>
            </div>
        </form>
    </div>

    <!-- Alertas -->
    {#if mensajeError}
        <div class="alert-error">
            <blink>⚠️ ¡ERROR! ⚠️</blink><br>
            {mensajeError}
        </div>
    {/if}

    {#if mensajeExito}
        <div class="alert-success">
            ✨ ¡ÉXITO! ✨<br>
            {mensajeExito} 
            {#if raiz !== null}
                <br><b>Raíz aproximada: <span style="font-size: 24px;">{raiz.toFixed(8)}</span></b>
            {/if}
        </div>
    {/if}

    <!-- Tabla de Resultados -->
    {#if resultados.length > 0}
        <div class="retro-panel">
            <h2 style="text-align: center; text-decoration: underline; margin-top: 0;">Resultados del Cálculo</h2>
            <table class="retro-table">
                <thead>
                    <tr>
                        <th>Iteración</th>
                        <th>xᵢ</th>
                        <th>f(xᵢ)</th>
                        <th>f'(xᵢ)</th>
                        <th>Error Relativo</th>
                    </tr>
                </thead>
                <tbody>
                    {#each resultados as fila}
                        <tr>
                            <td><b>{fila.paso}</b></td>
                            <td style="font-family: monospace;">{fila.x_actual.toFixed(8)}</td>
                            <td style="font-family: monospace;">{fila.f_x.toExponential(4)}</td>
                            <td style="font-family: monospace;">{fila.f_derivada_x.toFixed(6)}</td>
                            <td style="font-family: monospace;">
                                {fila.error_relativo !== null ? fila.error_relativo.toExponential(4) : 'N/A'}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
        
        <div style="text-align: center;">
            <img src="https://web.archive.org/web/20091027005003im_/http://www.geocities.com/Heartland/Plains/1105/undercon.gif" alt="Under Construction" style="max-width: 100px;">
            <p style="font-size: 10px;">Copyright © 2003 NewtonRaphsonWeb. Todos los derechos reservados.</p>
        </div>
    {/if}

</div>