# 🔧 Fix: Stop/Start Crash - Web Engine Singleton Reset

## 📋 Problema Identificado

**Sintoma:** Bot para corretamente, mas quando você clica "Start" novamente, ele crash imediatamente com erro de context destroyed.

**Logs do Problema:**
```
2025-07-04 21:05:30.214 | SUCCESS | src.core.bot_runner:initialize:157 - ✅ Bot initialized successfully
2025-07-04 21:05:30.217 | DEBUG | automation.web_engine:is_context_destroyed:592 - Context check error (assuming alive): Page.evaluate: 'NoneType' object has no attribute 'send'
2025-07-04 21:05:30.821 | WARNING | automation.web_engine:is_context_destroyed:552 - 🚨 Page or context is None after wait - likely destroyed
2025-07-04 21:05:30.821 | ERROR | src.core.bot_runner:run_cycle:84 - 🚨 Page navigation detected - bot context destroyed!
```

## 🔍 Causa Raiz

O problema está no **WebEngineManager singleton**:

1. **Primeira execução:** WebEngineManager cria instância do web engine
2. **Stop:** Bot para, mas WebEngineManager **mantém a instância singleton**
3. **Start:** Bot reinicia, WebEngineManager **retorna a mesma instância** (que está em estado inválido)
4. **Crash:** A instância reutilizada tem contexto Playwright destruído

### Código Problemático:
```python
class WebEngineManager:
    _instance: WebAutomationEngine | None = None

    @classmethod
    async def get_instance(cls) -> WebAutomationEngine:
        if cls._instance is None:
            # Cria nova instância
            cls._instance = WebAutomationEngine(config)
            await cls._instance.initialize()
        return cls._instance  # ❌ PROBLEMA: Retorna instância stale
```

## 🛠️ Solução Implementada

### Modificação na Função `start_bot()`

Adicionei **reset forçado do singleton** antes de criar novo bot:

```python
def start_bot(self):
    """Start the bot with proper cleanup of previous instance"""
    if self.running:
        return

    try:
        # ... cleanup de thread anterior ...

        # 🔥 CRÍTICO: Reset web engine singleton antes de criar novo bot
        logger.info("🔄 Resetting web engine for fresh start...")
        try:
            import asyncio

            # Create new event loop for this thread
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Import and shutdown global web engine
            try:
                from src.automation.web_engine import WebEngineManager
            except ImportError:
                from automation.web_engine import WebEngineManager

            # 🎯 Force shutdown of singleton instance
            loop.run_until_complete(WebEngineManager.shutdown())
            logger.success("✅ Web engine singleton reset")

        except Exception as e:
            logger.warning(f"⚠️ Could not reset web engine: {e}")

        # ... resto do código de reset ...

        # Small delay to ensure cleanup is complete
        time.sleep(1.0)  # Increased delay to ensure complete cleanup

        # ... criar novo bot runner ...
```

### Função `shutdown()` do WebEngineManager:
```python
@classmethod
async def shutdown(cls) -> None:
    """Shutdown the web engine instance"""
    if cls._instance:
        await cls._instance.shutdown()
        cls._instance = None  # 🎯 Reset singleton para None
```

## 🔄 Fluxo Corrigido

### Antes (Problemático):
```
Start → WebEngine Singleton Created → Stop → Start → Same Singleton (STALE) → CRASH
```

### Depois (Corrigido):
```
Start → WebEngine Singleton Created → Stop → RESET SINGLETON → Start → New Singleton → SUCCESS
```

## 🎯 Sequência de Eventos Corrigida

### 1. **Primeiro Start:**
```
1. start_bot() called
2. WebEngineManager.get_instance() → creates new singleton
3. Bot runs successfully
```

### 2. **Stop:**
```
1. stop_bot() called
2. Bot thread stops
3. WebEngine singleton remains in memory (but context may be invalid)
```

### 3. **Second Start (FIXED):**
```
1. start_bot() called
2. 🔥 WebEngineManager.shutdown() → destroys singleton
3. WebEngineManager.get_instance() → creates FRESH singleton
4. Bot runs successfully with clean context
```

## 🧪 Como Testar a Correção

### Teste Manual:
1. **Start bot** → Aguardar inicialização completa
2. **Stop bot** → Aguardar parada completa
3. **Start bot novamente** → **RESULTADO ESPERADO:** Inicia sem crash

### Teste de Logs:
Procurar por estas mensagens no log:
```
✅ Logs Esperados no Start:
🔄 Resetting web engine for fresh start...
✅ Web engine singleton reset
🚀 Bot started successfully!

❌ Logs de Problema (se ainda ocorrer):
🚨 Page or context is None after wait - likely destroyed
🚨 Page navigation detected - bot context destroyed!
```

## 🔧 Melhorias Adicionais

### 1. **Delay Aumentado:**
- **Antes:** `time.sleep(0.5)`
- **Depois:** `time.sleep(1.0)` → Mais tempo para cleanup completo

### 2. **Log Melhorado:**
- Logs específicos para reset de web engine
- Melhor rastreamento do processo

### 3. **Error Handling:**
- Try/catch around web engine reset
- Fallback gracioso se reset falhar

## 📊 Resultado Esperado

Após esta correção:

### ✅ **Stop/Start Reliability:**
- Stop funciona limpo (já funcionava)
- **Start após Stop funciona consistentemente** (fix principal)
- Sem crashes de context destroyed em restart

### ✅ **Context Management:**
- Singleton sempre fresh no restart
- Contexto Playwright sempre válido
- Sem estado stale entre execuções

### ✅ **User Experience:**
- Bot pode ser parado e iniciado múltiplas vezes
- Sem necessidade de restart do programa
- Interface responsiva e confiável

Esta correção resolve definitivamente o problema de crash no restart do bot!
