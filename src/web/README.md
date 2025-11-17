# Movie Recommendation Platform - Web Frontend

Interface web da plataforma de recomendação de filmes, desenvolvida com React, TypeScript, Vite e Tailwind CSS.

## 🚀 Como Executar

### Pré-requisitos

- Node.js 18+ instalado
- npm ou yarn

### Passos para Iniciar a Aplicação

1. **Navegar para o diretório web**

   ```powershell
   cd src\web
   ```

2. **Instalar dependências** (apenas na primeira vez)

   ```powershell
   npm install
   ```

3. **Iniciar o servidor de desenvolvimento**

   ```powershell
   npm run dev
   ```

4. **Abrir no browser**

   A aplicação irá iniciar automaticamente e estará disponível em:

   **http://localhost:5173**

   Abra este endereço no seu browser preferido (Chrome, Firefox, Edge, etc.)

### Outros Comandos Úteis

```powershell
# Build de produção
npm run build

# Executar linting
npm run lint

# Preview do build de produção
npm run preview
```

## 🏗️ Estrutura do Projeto

```
src/web/
├── src/
│   ├── components/      # Componentes React reutilizáveis
│   │   ├── carousel.tsx
│   │   ├── movieCard.tsx
│   │   ├── movieTable.tsx
│   │   ├── navbar.tsx
│   │   └── searchInput.tsx
│   ├── pages/          # Páginas da aplicação
│   │   ├── authPage.tsx
│   │   ├── browsePage.tsx
│   │   ├── homePage.tsx
│   │   ├── ratingsPage.tsx
│   │   └── wishlistPage.tsx
│   ├── routes/         # Configuração de rotas
│   │   └── AppRoutes.tsx
│   ├── App.tsx         # Componente principal
│   ├── main.tsx        # Entry point
│   └── index.css       # Estilos globais
├── public/             # Assets estáticos
├── index.html
└── package.json
```

## 🛠️ Stack Tecnológica

- **React 19** - Framework UI
- **TypeScript** - Type safety
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Styling
- **React Router** - Navegação
- **Swiper** - Carousel de filmes
- **Lucide React** - Ícones

## 📝 Notas

- O servidor de desenvolvimento tem hot-reload ativado, todas as alterações são refletidas automaticamente
- A API backend deve estar a correr em `http://localhost:5000` para funcionalidade completa
- Para produção, executar `npm run build` e servir os ficheiros da pasta `dist/`
