"""
📋 Instruções Completas - Login Manual + Bot

Este arquivo contém as instruções passo-a-passo para:
1. Fazer login manual sem interferência do bot
2. Conectar o bot ao browser já logado
"""

from loguru import logger


def show_instructions():
    """Mostra instruções completas"""
    logger.info("📋 INSTRUÇÕES COMPLETAS - Login Manual + Bot")
    logger.info("=" * 60)

    logger.info("")
    logger.info("🎯 OBJETIVO:")
    logger.info("   Fazer login manual primeiro, depois conectar o bot")
    logger.info("   ao browser já logado para evitar problemas com Cloudflare")
    logger.info("")

    logger.info("📝 PASSO 1: Login Manual (COM debugging)")
    logger.info("   Command: python manual_profile_launcher.py")
    logger.info("   • Abre browser com perfilteste + debugging port 9222")
    logger.info("   • Você faz login completamente manual")
    logger.info("   • Vai direto para página travel")
    logger.info("   • Debugging já habilitado para bot conectar depois")
    logger.info("")

    logger.info("📝 PASSO 2: Completar Login")
    logger.info("   No browser que abriu:")
    logger.info("   • Complete o challenge do Cloudflare")
    logger.info("   • Faça login na sua conta SimpleMMO")
    logger.info("   • Navegue para a página de travel")
    logger.info("   • Verifique se vê botões 'Take a step'")
    logger.info("   • MANTENHA o browser aberto!")
    logger.info("")

    logger.info("📝 PASSO 3: Conectar Bot (NOVO Sistema Inteligente)")
    logger.info("   Command: python start_bot_with_debugging.py")
    logger.info("   • Conecta ao browser já aberto na porta 9222")
    logger.info("   • Detecta login automático")
    logger.info("   • NOVO: Aguarda botões ficarem disponíveis")
    logger.info("   • NOVO: Evita navegações desnecessárias")
    logger.info("   • Executa steps de forma mais eficiente")
    logger.info("")

    logger.info("🧪 TESTES DISPONÍVEIS:")
    logger.info("   • python test_quick_steps.py    - Teste rápido (3 steps)")
    logger.info("   • python test_smart_steps.py    - Teste completo")
    logger.info("")

    logger.info("🔍 TESTE DE DEBUG (opcional):")
    logger.info("   Command: python test_debug_port.py")
    logger.info("   • Verifica se porta 9222 está ativa")
    logger.info("   • Mostra tabs abertas no browser")
    logger.info("")

    logger.info("✅ VANTAGENS desta abordagem:")
    logger.info("   • Login 100% manual = sem detecção")
    logger.info("   • Bot conecta depois = sem Cloudflare")
    logger.info("   • Perfil persistente = login salvo")
    logger.info("   • Separação clara entre login e bot")
    logger.info("   • NOVO: Espera inteligente por botões")
    logger.info("   • NOVO: Menos navegações desnecessárias")
    logger.info("")

    logger.info("⚠️ IMPORTANTE:")
    logger.info("   • NÃO feche o browser entre os passos")
    logger.info("   • Execute os scripts na ordem correta")
    logger.info("   • Aguarde login completo antes do passo 3")
    logger.info("")

    logger.info("🔧 SCRIPTS DISPONÍVEIS:")
    logger.info("   1. manual_profile_launcher.py    - Login manual")
    logger.info("   2. start_bot_with_debugging.py   - Conectar bot (NOVO)")
    logger.info("   3. test_quick_steps.py          - Teste rápido")
    logger.info("   4. test_smart_steps.py          - Teste completo")
    logger.info("   5. test_cloudflare.py           - Testar Cloudflare")
    logger.info("   6. demo_bot_completo.py         - Método antigo")
    logger.info("")


def main():
    """Função principal"""
    show_instructions()

    logger.info("🤔 Escolha uma opção:")
    logger.info("   1. Começar processo (Passo 1)")
    logger.info("   2. Conectar bot (Passo 3)")
    logger.info("   3. Apenas mostrar instruções")
    logger.info("   4. Sair")

    choice = input("\n👉 Digite sua escolha (1-4): ").strip()

    if choice == "1":
        logger.info("🚀 Iniciando Passo 1...")
        import subprocess
        subprocess.run(["python", "manual_profile_launcher.py"], check=False)
    elif choice == "2":
        logger.info("🚀 Iniciando Passo 3...")
        import subprocess
        subprocess.run(["python", "start_bot_with_debugging.py"], check=False)
    elif choice == "3":
        logger.info("📋 Instruções mostradas acima")
    elif choice == "4":
        logger.info("👋 Saindo...")
    else:
        logger.warning("⚠️ Opção inválida")


if __name__ == "__main__":
    main()
