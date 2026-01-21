# 使用指南 | User Guide

## 快速开始 | Quick Start

### 1. 安装依赖 | Install Dependencies

```bash
# 使用自动安装脚本 | Use automatic setup script
./setup.sh

# 或手动安装 | Or install manually
pip install -r requirements.txt
```

### 2. 配置邮箱 | Configure Email

复制配置示例文件并编辑：
Copy example config and edit:

```bash
cp config.example.env config.env
nano config.env
```

配置内容 | Configuration:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
RECIPIENT_EMAIL=your-email@gmail.com
SCHEDULE_TIME=09:00
```

### 3. 运行系统 | Run System

#### 单次检查 | One-time Check
```bash
python main.py --once
```

#### 每日定时检查 | Daily Scheduled Checks
```bash
python main.py
```

#### 使用 Docker | Using Docker
```bash
# 构建并运行 | Build and run
docker-compose up -d

# 查看日志 | View logs
docker-compose logs -f

# 停止 | Stop
docker-compose down
```

## 支持的签证类型 | Supported Visa Types

### 🇫🇷 法国申根签证 | France Schengen Visa
- **中心**: TLS Contact 香港 | TLS Contact Hong Kong
- **网站**: https://cn.tlscontact.com/hk/HKG/page.php?pid=tourism

### 🇺🇸 美国签证 | US Visa
- **中心**: 美国驻香港总领事馆 | US Consulate General Hong Kong  
- **网站**: https://ais.usvisa-info.com/en-hk/niv

### 🇦🇺 澳洲签证 | Australia Visa
- **中心**: VFS Global 香港 | VFS Global Hong Kong
- **网站**: https://www.vfsglobal.com/en/individuals/australia.html

## 邮件报告示例 | Email Report Sample

系统会每天发送格式化的HTML邮件，包含：
The system sends daily formatted HTML emails containing:

- ✅ 签证预约状态 | Visa appointment status
- 📅 最早可预约日期 | Earliest available date
- 🔗 预约网站链接 | Booking website links
- ⏰ 检查时间 | Check timestamp

## 常见问题 | FAQ

### Gmail 配置 | Gmail Setup

1. 开启两步验证 | Enable 2-Step Verification
2. 生成应用专用密码 | Generate App Password
3. 使用应用密码作为 SMTP_PASSWORD | Use app password as SMTP_PASSWORD

### 添加新国家 | Adding New Countries

1. 创建新的检查器类 | Create new checker class
2. 在 main.py 中注册 | Register in main.py
3. 添加配置选项 | Add configuration option

### 系统服务 | System Service

```bash
# 安装服务 | Install service
sudo cp hkvisa.service /etc/systemd/system/
sudo systemctl enable hkvisa
sudo systemctl start hkvisa

# 查看状态 | Check status
sudo systemctl status hkvisa
```

## 技术架构 | Technical Architecture

- **语言 | Language**: Python 3.7+
- **调度 | Scheduling**: schedule 库 | schedule library
- **邮件 | Email**: SMTP (支持 Gmail, Outlook 等 | supports Gmail, Outlook, etc.)
- **部署 | Deployment**: 支持直接运行、Docker、systemd | Direct, Docker, systemd

## 安全提示 | Security Tips

- ✅ 使用应用专用密码 | Use app-specific passwords
- ✅ 不要提交 config.env | Never commit config.env
- ✅ 定期更新依赖 | Regularly update dependencies
- ✅ 遵守网站使用条款 | Respect website terms of service
