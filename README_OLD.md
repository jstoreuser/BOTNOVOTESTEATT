# 👣 SimpleMMO Step**## 🔓 **IMPORTANTE: Solução Cloudflare (LEIA PRIMEIRO)**

⚡ **O SimpleMMO usa Cloudflare que bloqueia automação normal. Use esta solução em 2 passos:**

### 🥇 **MÉTODO RECOMENDADO: Login Manual + Bot**

```bash
# PASSO 1: Login manual (SEM bot)
python manual_profile_launcher.py
```
- ✅ Abre browser limpo com perfilteste
- ✅ SEM flags de debugging ou automação
- ✅ Você faz login completamente manual
- ✅ Completa Cloudflare challenge sem interferência

```bash
# PASSO 2: Conectar bot (APÓS login completo)
python start_bot_with_debugging.py
```
- ✅ Conecta ao browser já logado
- ✅ Executa bot automaticamente
- ✅ Sem problemas de Cloudflare

### �📋 **Instruções Detalhadas**
```bash
# Para instruções passo-a-passo completas
python instructions.py
```

---

### 🔄 **Método Alternativo: Demo Completo**

```bash
# Execute o bot demo completo (método antigo)
python demo_bot_completo.py
```ompleto:**
1. 🚀 Inicia browser com perfilteste
2. 🔗 Testa conexão com browser em execução
3. 🤖 Executa bot conectado ao browser
4. 🏃 **QUICK START** (automático)
5. ❌ Sair

### 🛡️ Se o Cloudflare ainda bloquear:

```bash
# Use o launcher ultra-stealth
python ultra_stealth_browser.py
```

**Configurações ultra-stealth para bypass:**
- ✅ Flags anti-detecção máximos
- ✅ User agent natural
- ✅ Timing humano de carregamento
- ✅ Profile persistente com login salvo Modern Edition

Bot moderno para SimpleMMO com foco em steps, usando **Playwright** e interface gráfica com **DearPyGUI**.

## � **IMPORTANTE: Solução Cloudflare (LEIA PRIMEIRO)**

⚡ **O SimpleMMO usa Cloudflare que bloqueia automação normal. Use esta solução:**

```bash
# Execute o bot demo completo (RECOMENDADO)
python demo_bot_completo.py
```

**✅ Configuração automática com perfilteste:**
- **Opção 4** (Quick Start): Inicia browser + executa bot automaticamente
- Perfil "perfilteste" do Chromium do Playwright já criado e com login salvo
- Caminho: `C:\Users\jesse\AppData\Local\ms-playwright\chromium-1179\chrome-win\`
- Sem problemas de Cloudflare ou captcha!

**📋 Menu completo:**
1. 🚀 Inicia browser com perfilteste
2. 🔗 Testa conexão com browser em execução
3. 🤖 Executa bot conectado ao browser
4. 🏃 **QUICK START** (automático)
5. ❌ Sair

---

## �🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar Interface Gráfica
```bash
python step_bot_gui.py
```

### 3. Ou Executar Bot Simples (Terminal)
```bash
python simple_step_bot.py
```

## 🎮 Interface Gráfica

A interface oferece:

- **🚀 Start Bot**: Inicia o bot automático
- **🛑 Stop Bot**: Para o bot
- **🔄 Take Single Step**: Executa um único step para teste
- **📊 Estatísticas**: Mostra steps executados, sucessos e falhas
- **📝 Logs**: Log em tempo real das ações do bot
- **⚙️ Configurações**: Ajustar ciclos máximos e delay entre steps

## 🔧 Arquitetura

### Tecnologias Modernas
- **Playwright**: Automação web moderna (substitui Selenium)
- **Async/Await**: Performance otimizada
- **DearPyGUI**: Interface nativa e responsiva
- **Loguru**: Logging avançado e colorido

### Estrutura Modular
```
src/
├── core/
│   ├── steps.py        # Sistema de steps principal
│   ├── web_engine.py   # Motor de automação web
│   ├── combat.py       # Sistema de combate (futuro)
│   ├── gathering.py    # Sistema de coleta (futuro)
│   ├── healing.py      # Sistema de cura (futuro)
│   └── captcha.py      # Detecção de captcha (futuro)
├── ui/
│   └── gui.py          # Interface principal (futuro)
└── utils/
    ├── config.py       # Configurações
    └── logging.py      # Sistema de logs
```

## 🎯 Funcionalidades Atuais

### ✅ Sistema de Steps
- Detecção inteligente de botões "Take a step"
- Múltiplas estratégias de detecção (fallbacks)
- Navegação automática para página de travel
- Timing humano para evitar detecção
- Estatísticas detalhadas

### 🔄 Próximas Implementações
- Sistema de combate
- Sistema de coleta
- Sistema de cura
- Detecção de captcha
- AI para decisões inteligentes

## ⚙️ Configurações

Edite as configurações no topo dos arquivos:

```python
config = {
    "browser_headless": False,    # True para executar sem interface
    "step_delay_min": 1.0,        # Delay mínimo entre steps
    "step_delay_max": 2.0,        # Delay máximo entre steps
}
```

## 🛡️ Recursos Anti-Detecção

- **Timing Humano**: Delays variáveis e realistas
- **Múltiplas Estratégias**: Fallbacks para maior confiabilidade
- **Playwright Stealth**: Browser mode otimizado
- **Patterns Inteligentes**: Evita padrões robotizados

## 🐛 Solução de Problemas

### Bot não encontra botões
1. Verifique se está na página de travel do SimpleMMO
2. Certifique-se que há steps disponíveis
3. Verifique os logs para detalhes do erro

### Interface não abre
1. Certifique-se que DearPyGUI está instalado: `pip install dearpygui`
2. Execute: `python -c "import dearpygui; print('OK')"`

### Problemas com Playwright
1. Instale browsers: `playwright install`
2. Verifique permissões do antivírus

## 📊 Exemplo de Uso

1. Abra `step_bot_gui.py`
2. Ajuste configurações (ciclos máximos, delay)
3. Clique "🚀 Start Bot"
4. Acompanhe logs e estatísticas
5. Use "🛑 Stop Bot" quando necessário

## 🔮 Roadmap

- [ ] Sistema de combate completo
- [ ] Sistema de coleta automática
- [ ] AI para decisões inteligentes
- [ ] Dashboard web (opcional)
- [ ] Notificações push
- [ ] Profiles/configurações salvas
- [ ] Modo de training/learning

---

**Desenvolvido com 💖 para a comunidade SimpleMMO**
