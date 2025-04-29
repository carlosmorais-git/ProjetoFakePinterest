import os
import shutil
import subprocess
import time

# ⚙️ Configurações
CAMINHO_DB = r'C:\Users\carlo\Documents\GitHub\ProjetoFakePinterest\instance\bancoDB.db'  # Altere se o nome do seu .db for diferente
CAMINHO_MIGRATIONS = 'migrations'
CAMINHO_FOTOS = os.path.join('projeto\static', 'fotos_posts')  # Ou ajuste conforme onde salva suas fotos
APAGAR_FOTOS = True  # Se quiser apagar as fotos também, deixa True. Se não, coloca False.

def deletar_arquivo(caminho):
    if os.path.exists(caminho):
        os.remove(caminho)
        print(f"✅ Arquivo deletado: {caminho}")
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho}")

def deletar_pasta(caminho):
    if os.path.exists(caminho):
        shutil.rmtree(caminho)
        print(f"✅ Pasta deletada: {caminho}")
    else:
        print(f"⚠️ Pasta não encontrada: {caminho}")

def rodar_comando(cmd):
    print(f"▶️ Executando: {cmd}")
    resultado = subprocess.run(cmd, shell=True)
    if resultado.returncode == 0:
        print("✅ Comando executado com sucesso.\n")
    else:
        print("❌ Erro ao executar comando.\n")

def main():
    print("\n🧹 Resetando Banco de Dados e Migrations...\n")
    time.sleep(1)

    deletar_arquivo(CAMINHO_DB)
    deletar_pasta(CAMINHO_MIGRATIONS)

    if APAGAR_FOTOS:
        deletar_pasta(CAMINHO_FOTOS)

    # Inicializar o Migrations do zero
    rodar_comando('flask --app projeto db init')

    # Criar nova migração
    rodar_comando('flask --app projeto db migrate -m "estrutura inicial"')

    # Aplicar migração no novo banco
    rodar_comando('flask --app projeto db upgrade')

    print("🎉 Banco de dados resetado com sucesso!\n")

if __name__ == "__main__":
    main()
