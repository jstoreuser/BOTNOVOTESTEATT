# 🧪 Scripts de Teste - SimpleMMO Bot v5.0.0

Esta pasta contém scripts de teste para validar diferentes componentes do bot.

> **✅ Atualização Recente:** Sistemas otimizados com performance EXCELLENT (100/100)! Todos os imports corrigidos para usar `botlib` ao invés de imports diretos do `src/`.

## 📊 Performance Otimizada

### 🏆 Score: 100/100 EXCELLENT
- **⚡ Actions/sec**: 2.0 (gathering e combat)
- **🔍 Button checks**: 20/segundo (50ms response)
- **⏱️ Max timeout**: 3.0s (otimizado)
- **📈 Overall Grade**: 🏆 EXCELLENT

### test_performance.py
Teste completo de performance dos sistemas otimizados.

```bash
python scripts/tests/test_performance.py
```

### test_optimized_systems.py
Verifica se os timings dos sistemas estão consistentes e otimizados.

```bash
python scripts/tests/test_optimized_systems.py
```

## 🤖 Testes de Automação

### test_gathering.py
Testa o sistema completo de gathering otimizado que detecta oportunidades de coleta (chop, mine, salvage, catch), executa múltiplos cliques e retorna para travel.

```bash
python scripts/tests/test_gathering.py
```

### test_combat.py
Testa o sistema completo de combate otimizado que detecta inimigos, entra em combate, ataca até o HP zerar e retorna para travel.

```bash
python scripts/tests/test_combat.py
```

### test_smart_steps.py
Testa o novo sistema de steps com espera inteligente que aguarda o botão "Take a step" ficar disponível.

```bash
python scripts/tests/test_smart_steps.py
```

### test_quick_steps.py
Teste rápido do sistema de steps. Execute após fazer login manual com o `manual_profile_launcher.py`.

```bash
python scripts/tests/test_quick_steps.py
```

## 🎮 Testes de Interface

### test_gui.py
Teste simples para verificar se a interface DearPyGUI está funcionando corretamente.

```bash
python scripts/tests/test_gui.py
```

## 🔧 Testes de Depuração

### test_debug_port.py
Testa se conseguimos nos conectar ao Chrome via CDP (Chrome DevTools Protocol).

```bash
python scripts/tests/test_debug_port.py
```

## 🌐 Testes de Playwright

### simple_playwright_test.py
Teste básico do Playwright para verificar se a integração está funcionando.

```bash
python scripts/tests/simple_playwright_test.py
```

### test_cloudflare.py
Testa se o bot consegue lidar com proteções do Cloudflare.

```bash
python scripts/tests/test_cloudflare.py
```

## 📋 Como Executar os Testes

1. **Certifique-se de que o ambiente está configurado:**
   ```bash
   # Execute o setup se ainda não executou
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Para testes de GUI:**
   ```bash
   python scripts/tests/test_gui.py
   ```

3. **Para testes de automação (requer login manual primeiro):**
   ```bash
   # 1. Primeiro faça login manual
   python scripts/launchers/manual_profile_launcher.py

   # 2. Em seguida execute o teste
   python scripts/tests/test_quick_steps.py
   ```

4. **Para testes standalone (não requerem login):**
   ```bash
   python scripts/tests/test_debug_port.py
   python scripts/tests/simple_playwright_test.py
   ```

## 🔍 Estrutura dos Testes

- **Interface**: Testes de GUI e componentes visuais
- **Automação**: Testes de funcionalidade core do bot
- **Depuração**: Testes para diagnóstico e resolução de problemas
- **Playwright**: Testes específicos do driver de automação

## 📝 Notas

- Os testes de automação requerem que o bot esteja conectado ao Chrome
- Para testes de GUI, certifique-se de que não há outras janelas DearPyGUI abertas
- Os testes não modificam dados reais do jogo, apenas verificam funcionalidades
