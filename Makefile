# 🛠️ Makefile Simplificado - Solo comandos únicos
# Para desarrolladores que prefieren make sobre pdm

.PHONY: help setup quick-start dev-setup

# Comando por defecto
help:
	@echo "🚀 MCP Server Template - Comandos Make Disponibles:"
	@echo ""
	@echo "  help         - 📋 Mostrar esta ayuda"
	@echo "  setup        - 🔧 Configuración inicial completa"
	@echo "  quick-start  - ⚡ Inicio rápido (solo producción)"
	@echo "  dev-setup    - 🛠️ Configuración completa para desarrollo"
	@echo ""
	@echo "💡 Para comandos diarios, usa: pdm run <comando>"
	@echo "   pdm run start    - Ejecutar servidor"
	@echo "   pdm run test     - Ejecutar pruebas"
	@echo "   pdm run new-tool - Crear herramienta"

# Configuración inicial completa (primera vez)
setup: dev-setup
	@echo "✅ ¡Configuración completa! Usa 'pdm run start' para iniciar."

# Inicio rápido solo producción
quick-start:
	@echo "⚡ Configuración rápida..."
	pdm install --prod
	@echo "✅ ¡Listo! Usa 'pdm run start' para iniciar."

# Configuración completa para desarrollo
dev-setup:
	@echo "🛠️ Configurando entorno de desarrollo completo..."
	pdm install -G dev,examples
	@echo "✅ ¡Entorno de desarrollo listo!"
