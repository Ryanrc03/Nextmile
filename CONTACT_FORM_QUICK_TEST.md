# 联系表单快速测试指南

## 🚀 快速测试命令

### 测试生产环境
```bash
curl -X POST https://nextmile.space/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "测试",
    "lastName": "用户",
    "emailId": "test@example.com",
    "mobNo": "+1234567890",
    "message": "这是一条测试消息"
  }' | jq .
```

**预期结果：**
```json
{
  "message": "Email sent successfully",
  "messageId": "<xxxxx@gmail.com>"
}
```

### 检查容器日志
```bash
sudo docker logs nextmile_frontend --tail 20
```

**预期输出应包含：**
```
=== Contact Form Submission ===
Environment check:
- EMAIL_USER: SET
- EMAIL_PASS: SET (length: 16)
- NODE_ENV: production
Email config found, creating transporter...
SMTP connection verified
Sending email...
Email sent successfully: <xxxxx@gmail.com>
```

## 🔧 故障排查

### 问题 1: 404 Not Found
**症状：** `{"detail":"Not Found"}`

**原因：** NGINX 配置错误，请求被路由到 FastAPI 而不是 Next.js

**解决方案：**
```bash
# 检查 NGINX 配置
sudo cat /etc/nginx/conf.d/nextmile.space.conf | grep -A 5 "location /api/contact"

# 应该看到：
# location /api/contact {
#     proxy_pass http://localhost:3000;
#     ...
# }

# 如果没有，更新配置：
sudo cp /home/ec2-user/Nextmile/nginx/nextmile.space.conf /etc/nginx/conf.d/
sudo nginx -t && sudo systemctl reload nginx
```

### 问题 2: 500 Internal Server Error
**症状：** `{"error":"Email configuration not found"}`

**原因：** 环境变量未正确加载

**解决方案：**
```bash
# 检查容器环境变量
sudo docker exec nextmile_frontend env | grep EMAIL

# 应该看到：
# EMAIL_USER=ryanrc230107@gmail.com
# EMAIL_PASS=xxxxx

# 如果没有，重启容器：
cd /home/ec2-user/Nextmile
sudo docker-compose restart frontend
```

### 问题 3: SMTP Connection Failed
**症状：** `{"error":"Email server connection failed"}`

**原因：** Gmail 凭据错误或网络问题

**解决方案：**
```bash
# 验证 .env 文件
cat /home/ec2-user/Nextmile/.env

# 确保：
# 1. EMAIL_USER 是正确的 Gmail 地址
# 2. EMAIL_PASS 是 Gmail App Password (16个字符)
# 3. 没有多余的空格或引号

# 更新后重启：
cd /home/ec2-user/Nextmile
sudo docker-compose restart frontend
```

## 📊 关键文件位置

| 文件 | 路径 |
|------|------|
| 联系表单页面 | `/home/ec2-user/Nextmile/Frontend/app/contact/page.tsx` |
| API 路由 | `/home/ec2-user/Nextmile/Frontend/app/api/contact/route.ts` |
| NGINX 配置 (源) | `/home/ec2-user/Nextmile/nginx/nextmile.space.conf` |
| NGINX 配置 (生效) | `/etc/nginx/conf.d/nextmile.space.conf` |
| Docker Entrypoint | `/home/ec2-user/Nextmile/Frontend/docker-entrypoint.sh` |
| 环境变量 | `/home/ec2-user/Nextmile/.env` |

## 🌐 访问链接

- **生产环境联系页面:** https://nextmile.space/ryan/contact
- **API 端点:** https://nextmile.space/api/contact
- **本地测试:** http://localhost:3000/api/contact

## ✅ 健康检查清单

- [ ] NGINX 配置正确 (`/api/contact` 路由到 3000 端口)
- [ ] 容器日志显示环境变量已设置
- [ ] SMTP 连接验证成功
- [ ] 测试邮件成功发送
- [ ] 生产环境 API 返回 200 状态码
- [ ] 实际收到测试邮件

---
**最后更新:** 2025年10月6日  
**状态:** ✅ 完全正常工作
