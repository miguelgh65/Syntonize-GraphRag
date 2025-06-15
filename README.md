# 🧠 Syntonize GraphRAG Visualizer

<div align="center">
  <img src="public/demo.png" alt="GraphRAG Visualizer Demo" width="800"/>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![React](https://img.shields.io/badge/React-18.x-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
  [![Azure Static Web Apps](https://img.shields.io/badge/Azure-Static%20Web%20Apps-blue.svg)](https://azure.microsoft.com/en-us/services/app-service/static/)

  **Interactive Knowledge Graph Visualization for Microsoft GraphRAG**
  
  *Transform your culinary data into intelligent, queryable knowledge graphs*
</div>

## 🍳 About This Project

This project demonstrates the practical implementation of **Microsoft's GraphRAG** technology through a real-world culinary AI system. Inspired by the Pixar movie *Ratatouille* and the famous line "anyone can cook," we prove that **anyone can build knowledge graphs** when guided by the right AI assistant.

> 📖 **Read the full story**: [Anyone Can Build Knowledge Graphs: What I Learned Building a Culinary AI with Microsoft GraphRAG](#) *(Coming soon!)*

### 🎯 What Makes This Special?

- **🤖 AI-Powered Knowledge Extraction**: Automatically discovers relationships between ingredients, recipes, cooking methods, and nutritional values
- **🕸️ Interactive Graph Visualization**: Explore your data in stunning 2D/3D network graphs
- **🔍 Intelligent Search**: Both local and global search capabilities using GraphRAG's advanced algorithms  
- **📊 Rich Data Insights**: Visualize entities, relationships, communities, and findings
- **🏠 Privacy-First**: All processing happens locally - your data never leaves your machine

## ✨ Features

### 🎨 **Visual Exploration**
- **2D & 3D Graph Views**: Toggle between dimensions for optimal exploration
- **Interactive Node Details**: Click any node to explore its connections and metadata
- **Community Detection**: Automatically discovered clusters of related culinary concepts
- **Relationship Weighting**: Visual representation of connection strength

### 🔧 **Technical Capabilities**
- **Multiple Data Formats**: Support for entities, relationships, documents, text units, communities, and covariates
- **Real-time Search**: Fuzzy search across all graph elements
- **API Integration**: Connect to GraphRAG servers for live querying
- **Export/Import**: Work with standard Parquet files from GraphRAG processing

### 🍽️ **Culinary Intelligence**
Our demo dataset reveals fascinating insights:
- **Mediterranean Cluster**: Olive oil, garlic, tomatoes naturally group together
- **Protein & Nutrition Hub**: High-protein ingredients with nutritional correlations
- **Baking Ecosystem**: Flour-based dishes with temperature and technique relationships
- **Cooking Methods**: Sautéing, marinating, and grilling patterns

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Modern web browser with WebGL support

### Installation

```bash
# Clone the repository
git clone https://github.com/miguelgh65/Syntonize-GraphRag.git
cd Syntonize-GraphRag

# Install dependencies
npm install

# Start the development server
npm start
```

Visit `http://localhost:3000` and start exploring! 🎉

### 📂 Using Your Own Data

1. **Upload Artifacts**: Drag and drop your GraphRAG `.parquet` files
2. **Explore**: Switch to the Graph Visualization tab
3. **Discover**: Use search and filtering to uncover hidden patterns

## 📖 The Story Behind This Project

This visualizer was built as a companion to our article **"Anyone Can Build Knowledge Graphs: What I Learned Building a Culinary AI with Microsoft GraphRAG"**, where we explore:

- **🔬 The Science**: How GraphRAG's 7-phase pipeline transforms raw recipes into structured knowledge
- **🤝 The Partnership**: Microsoft's GraphRAG as our "digital Remy" (like the genius rat from Ratatouille)
- **📈 The Results**: Real insights discovered from 648 culinary documents
- **💡 The Lessons**: Practical tips for implementing GraphRAG in your own projects

### 🎬 The Ratatouille Connection

Just as Remy could see flavor combinations that humans missed, Microsoft's GraphRAG reveals hidden patterns in data that traditional extraction methods overlook. Our culinary AI discovered:

- **Technique Relationships**: "sautéing" → "softens" → "onion and garlic"
- **Ingredient Pairings**: "olive oil" → "enhances" → "gazpacho flavor" 
- **Equipment Requirements**: "non-stick pan" → "required for" → "sautéing technique"
- **Nutritional Correlations**: "olive oil" → "contributes" → "fats macronutrient"

## 🛠️ Technical Architecture

### Frontend Stack
- **React 18** with TypeScript for type-safe development
- **Material-UI** for polished, accessible components
- **Force Graph** libraries for 2D/3D network visualization
- **Hyparquet** for efficient Parquet file processing

### Graph Processing
- **Node Types**: Entities, Documents, Text Units, Communities, Findings, Covariates
- **Relationship Types**: RELATED, PART_OF, HAS_ENTITY, IN_COMMUNITY, HAS_FINDING
- **Community Detection**: Hierarchical Leiden Algorithm implementation
- **Search Capabilities**: Local semantic search and global community-based search

### Data Pipeline
```
Raw CSV → GraphRAG Processing → Parquet Files → React Visualizer → Interactive Insights
```

## 🌐 Live Demo & Deployment

### Azure Static Web Apps Deployment

This project is optimized for deployment on **Azure Static Web Apps** with:
- ✅ **Free tier eligible** - Perfect for personal projects
- ✅ **Automatic CI/CD** from GitHub
- ✅ **Global CDN** for fast loading worldwide
- ✅ **Custom domains** and HTTPS included

```bash
# Deploy to Azure (after configuring Static Web Apps)
npm run build
# Automatic deployment via GitHub Actions
```

## 🤝 Related Projects & Resources

### 📚 Essential Reading
- [Microsoft GraphRAG Documentation](https://microsoft.github.io/graphrag/)
- [GraphRAG: Enhancing RAG systems with Knowledge Graph Capabilities](https://medium.com/syntonize/graphrag-enhancing-rag-systems-with-knowledge-graph-capabilities-dc1cbd282783) - *Our theoretical foundation*
- [GraphRAG API Server](https://github.com/noworneverev/graphrag-api) - *For live search functionality*

### 🔗 GraphRAG Ecosystem
- **Original GraphRAG Visualizer**: [noworneverev/graphrag-visualizer](https://github.com/noworneverev/graphrag-visualizer)
- **Microsoft GraphRAG**: [microsoft/graphrag](https://github.com/microsoft/graphrag)
- **Community Contributions**: Growing ecosystem of GraphRAG tools and extensions

## 🎯 Use Cases

### 🏢 **Enterprise Applications**
- **Document Intelligence**: Extract insights from corporate knowledge bases
- **Research Analysis**: Discover patterns in scientific literature
- **Legal Discovery**: Map relationships in legal documents
- **Market Research**: Understand industry connections and trends

### 🎓 **Educational & Research**
- **Academic Research**: Visualize citation networks and concept relationships
- **Content Analysis**: Understand themes and patterns in large text corpora
- **Knowledge Management**: Create searchable, visual knowledge repositories

### 🍳 **Creative Projects**
- **Recipe Analysis**: Like our culinary demo - understand cooking patterns
- **Content Creation**: Discover content themes and inspiration
- **Trend Analysis**: Visualize emerging patterns in any domain

## 💫 What's Next?

- **🔄 Real-time Collaboration**: Multi-user graph exploration
- **📱 Mobile Optimization**: Touch-friendly mobile interface
- **🎨 Custom Styling**: Personalized graph appearance options
- **📊 Advanced Analytics**: Statistical analysis of graph properties
- **🔌 API Extensions**: More integration options with external services

## 🙏 Acknowledgments

- **Microsoft Research** for creating and open-sourcing GraphRAG
- **Pixar's Ratatouille** for the inspiring "anyone can cook" philosophy
- **Edamam API** for providing rich nutritional and recipe data
- **The GraphRAG Community** for continuous innovation and support

---

<div align="center">
  
  **Built with ❤️ by [Syntonize](https://github.com/miguelgh65)**
  
  *Turning complex data into beautiful, interactive knowledge*
  
  ⭐ **Star this repo if you found it helpful!** ⭐
  
</div>
