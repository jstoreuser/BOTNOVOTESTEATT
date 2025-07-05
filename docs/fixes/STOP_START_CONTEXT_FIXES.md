# 🔧 Stop/Start and Context Crash Fixes

## 📋 Problemas Identificados

### 1. Context Destruction Detection Fraco
**Problema:** A detecção de "execution context was destroyed" era muito básica e não capturava todos os casos de navegação.

**Logs observados:**
```
2025-07-04 20:41:09.996 | DEBUG | systems.steps:_take_step_comprehensive:415 - Comprehensive selector a:contains('step') failed: Page.query_selector: Execution context was destroyed, most likely because of a navigation.
```

### 2. Stop/Start Não Funcionava
**Problema:** Após clicar em Stop e depois Start, o bot não reiniciava corretamente.

**Causa:**
- Reset state executava em thread separada sem aguardar conclusão
- Start bot não aguardava reset completo antes de criar nova instância

### 3. Crash Handling Inadequado
**Problema:** Quando usuário mudava de página, bot continuava tentando operar e gerava erros contínuos.

## 🛠️ Correções Implementadas

### 1. Melhor Detecção de Context Destruction

**Arquivo:** `src/automation/web_engine.py`

```python
async def is_context_destroyed(self) -> bool:
    """Check if execution context was destroyed (navigation crash)"""
    try:
        # First check if we have basic objects
        if not self.page or not self.context:
            logger.warning("🚨 Page or context is None - destroyed")
            return True

        # Check if page is closed
        if self.page.is_closed():
            logger.warning("🚨 Page is closed - destroyed")
            return True

        # Try to get current URL - this often fails when context is destroyed
        current_url = self.page.url
        if not current_url or current_url == "about:blank":
            logger.warning("🚨 Page URL is blank or empty - likely destroyed")
            return True

        # Try a simple DOM operation to test if context is alive
        await self.page.evaluate("() => document.readyState")

        # Check if we're still on a SimpleMMO page
        if "simple-mmo.com" not in current_url:
            logger.warning(f"🚨 Page navigated away from SimpleMMO: {current_url}")
            return True

        return False

    except Exception as e:
        error_msg = str(e).lower()
        if any(phrase in error_msg for phrase in [
            "execution context was destroyed",
            "navigation",
            "target closed",
            "page closed",
            "browser closed",
            "context was destroyed"
        ]):
            logger.warning(f"🚨 Context destroyed detected: {e}")
            return True
        # For other errors, assume context is still alive but log the error
        logger.debug(f"Context check error (assuming alive): {e}")
        return False
```

**Melhorias:**
- ✅ Verifica se page/context existem
- ✅ Verifica se página está fechada
- ✅ Verifica se URL mudou para fora do SimpleMMO
- ✅ Testa operação DOM real
- ✅ Detecta múltiplos tipos de erro de contexto

### 2. Stop Bot com Reset Síncrono

**Arquivo:** `src/ui/modern_bot_gui.py`

```python
def stop_bot(self):
    """Stop the bot and reset all systems to initial state"""
    if not self.running:
        return

    try:
        self.running = False
        if self.bot_runner:
            self.bot_runner.running = False

        # Wait for thread to finish (with timeout)
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread.join(timeout=5.0)

        # Reset bot state immediately for fresh start
        if self.bot_runner:
            # Run reset synchronously to ensure it completes
            try:
                import asyncio

                # Create new event loop for this thread
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Run reset and wait for completion
                loop.run_until_complete(self.bot_runner.reset_state())
                logger.success("✅ Bot state reset completed")

            except Exception as e:
                logger.error(f"❌ Error resetting bot state: {e}")

        # Clear bot references
        self.bot_runner = None
        self.bot_thread = None
```

**Melhorias:**
- ✅ Reset executa sincronamente e aguarda conclusão
- ✅ Timeout aumentado para 5 segundos
- ✅ Referencias limpas após reset
- ✅ Log confirma reset completo

### 3. Start Bot com Cleanup Prévio

```python
def start_bot(self):
    """Start the bot with proper cleanup of previous instance"""
    if self.running:
        return

    try:
        # Ensure complete cleanup of previous bot instance
        if hasattr(self, 'bot_thread') and self.bot_thread and self.bot_thread.is_alive():
            logger.info("🔄 Waiting for previous bot thread to finish...")
            self.bot_thread.join(timeout=5.0)  # Wait up to 5 seconds
            if self.bot_thread.is_alive():
                logger.warning("⚠️ Previous bot thread still running - forcing new instance")

        # If there's an existing bot_runner, ensure it's reset
        if self.bot_runner:
            logger.info("🔄 Resetting previous bot runner state...")
            try:
                import asyncio

                # Create new event loop for this thread
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Run reset and wait for completion
                loop.run_until_complete(self.bot_runner.reset_state())
                logger.success("✅ Previous bot state reset completed")

            except Exception as e:
                logger.error(f"❌ Error resetting previous bot state: {e}")

        # Reset all state variables
        self.running = False
        self.paused = False
        self.bot_runner = None
        self.bot_thread = None

        # Small delay to ensure cleanup is complete
        import time
        time.sleep(0.5)
```

**Melhorias:**
- ✅ Aguarda thread anterior terminar
- ✅ Reset bot_runner anterior se existir
- ✅ Delay para garantir cleanup completo
- ✅ Estado limpo antes de criar nova instância

### 4. Crash Handling Melhorado

```python
def _handle_bot_crash(self, reason: str):
    """Handle bot crash by stopping it and updating UI"""
    logger.error(f"🚨 Bot crashed: {reason}")

    try:
        # Stop the bot immediately
        self.running = False
        if self.bot_runner:
            self.bot_runner.running = False

        # Clear references to crashed bot
        self.bot_runner = None
        self.bot_thread = None
        self.paused = False

        # Update UI to reflect crash and require manual restart
        self._update_button_states()
        self._update_status("🚨 Crashed - Manual Restart Required", "red")
        self._add_log(f"🚨 Bot crashed: {reason}")
        self._add_log("🛑 Bot stopped automatically due to page navigation")
        self._add_log("📝 Please check the browser page and restart when ready")

    except Exception as e:
        logger.error(f"Error handling bot crash: {e}")
```

**Melhorias:**
- ✅ Para bot imediatamente
- ✅ Limpa todas as referências
- ✅ UI mostra status claro de crash
- ✅ Instruções claras para usuário

## 🧪 Como Testar

### Teste 1: Context Destruction
1. Inicie o bot
2. Navegue para uma página diferente (ex: Google)
3. **Resultado esperado:** Bot para automaticamente com mensagem de crash

### Teste 2: Stop/Start
1. Inicie o bot
2. Clique em Stop
3. Aguarde mensagem "Bot stopped and reset"
4. Clique em Start
5. **Resultado esperado:** Bot inicia normalmente

### Teste 3: Navegação Acidental
1. Inicie o bot
2. No navegador, volte para página anterior ou mude URL
3. **Resultado esperado:** Bot detecta mudança e para automaticamente

## 📊 Resultados Esperados

Após essas correções:

### ✅ Context Destruction
- Bot detecta quando usuário navega para fora do SimpleMMO
- Para automaticamente sem gerar erros contínuos
- UI mostra status claro de crash

### ✅ Stop/Start Reliability
- Stop aguarda reset completo antes de finalizar
- Start aguarda cleanup completo antes de iniciar
- Sem conflitos entre instâncias antigas e novas

### ✅ Better User Experience
- Mensagens claras sobre o que aconteceu
- Instruções sobre quando reiniciar
- Sem loops de erro quando há problemas

### ✅ Logs Limpos
- Sem spam de "Execution context was destroyed"
- Logs informativos sobre o que está acontecendo
- Fácil diagnóstico de problemas

## 🔍 Detecção de Problemas

O bot agora detecta:
1. **Page/Context nulos**
2. **Página fechada**
3. **URL mudou para fora do SimpleMMO**
4. **Erros de contexto destruído**
5. **Navegação forçada pelo usuário**

E reage parando automaticamente e pedindo restart manual.
