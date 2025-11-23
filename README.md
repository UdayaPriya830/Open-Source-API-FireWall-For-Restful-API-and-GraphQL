# 🛡️ Open Source API Firewall - Advanced Protection

An intelligent, next-generation API security solution that protects both REST and GraphQL endpoints from cyber threats including SQL injection, XSS attacks, prompt injection, and GraphQL-specific exploits.

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/UdayaPriya830/Open-Source-API-FireWall-For-Restful-API-and-GraphQL.git
cd Open-Source-API-FireWall-For-Restful-API-and-GraphQL

# Install dependencies
pip install -r requirements.txt

# Start the firewall
python main.py

# Launch monitoring dashboard (in another terminal)
streamlit run dashboard.py
```

## 🔒 Security Features

- **SQL Injection Protection** - Advanced pattern matching
- **XSS Attack Prevention** - Comprehensive script injection detection
- **Prompt Injection Defense** - AI/LLM manipulation protection
- **GraphQL Security** - Query depth limiting and introspection blocking
- **AI-Powered Detection** - Machine learning anomaly detection
- **Real-time Monitoring** - Interactive dashboard with threat analytics

## 📊 Dashboard

Access the monitoring dashboard at `http://localhost:8501` after running:
```bash
streamlit run dashboard.py
```

## 🐳 Docker Deployment

```bash
docker build -t api-firewall .
docker run -p 8000:8000 -p 8501:8501 api-firewall
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](docs/)
- [Issues](https://github.com/UdayaPriya830/Open-Source-API-FireWall-For-Restful-API-and-GraphQL/issues)
- [Discussions](https://github.com/UdayaPriya830/Open-Source-API-FireWall-For-Restful-API-and-GraphQL/discussions)