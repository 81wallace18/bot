#!/bin/bash

echo "🚀 Iniciando build do Agente Criativa XYZ..."

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker compose down

# Limpar imagens antigas (opcional)
echo "🧹 Limpando imagens antigas..."
docker system prune -f

# Build das imagens
echo "🔨 Construindo imagens..."
docker compose build --no-cache

# Verificar se o build foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    echo "🚀 Iniciando containers..."
    docker compose up -d
    
    echo "📊 Status dos containers:"
    docker compose ps
    
    echo "🌐 URLs dos serviços:"
    echo "   - Agent Logic (Python): http://localhost:8000"
    echo "   - WhatsApp Handler: http://localhost:3000"
    echo "   - API Docs: http://localhost:8000/docs"
    
    echo "📝 Logs em tempo real:"
    echo "   docker compose logs -f"
else
    echo "❌ Erro no build. Verifique os logs acima."
    exit 1
fi 