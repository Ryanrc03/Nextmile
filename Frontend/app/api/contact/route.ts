import { NextRequest, NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

export async function POST(request: NextRequest) {
  try {
    const { firstName, lastName, mobNo, emailId, message } = await request.json();

    console.log('=== Contact Form Submission ===');
    console.log('Contact form submission:', { firstName, lastName, emailId, mobNo, message: message.substring(0, 50) + '...' });
    console.log('Environment check:');
    console.log('- EMAIL_USER:', process.env.EMAIL_USER ? 'SET' : 'NOT SET');
    console.log('- EMAIL_PASS:', process.env.EMAIL_PASS ? 'SET (length: ' + process.env.EMAIL_PASS.length + ')' : 'NOT SET');
    console.log('- NODE_ENV:', process.env.NODE_ENV);

    // 验证必填字段
    if (!firstName || !lastName || !emailId || !message) {
      console.log('Missing required fields');
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // 检查环境变量
    if (!process.env.EMAIL_USER || !process.env.EMAIL_PASS) {
      console.error('ERROR: Email configuration not found!');
      console.error('Available env vars:', Object.keys(process.env).filter(k => k.includes('EMAIL')));
      return NextResponse.json(
        { error: 'Email configuration not found. Please contact the administrator.' },
        { status: 500 }
      );
    }

    console.log('Email config found, creating transporter...');

    // 创建邮件传输器 (使用Gmail SMTP)
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS.replace(/\s/g, ''), // 移除空格
      },
      debug: true, // 启用调试
    });

    // 验证连接
    try {
      await transporter.verify();
      console.log('SMTP connection verified');
    } catch (verifyError) {
      console.error('SMTP verification failed:', verifyError);
      return NextResponse.json(
        { error: 'Email server connection failed' },
        { status: 500 }
      );
    }

    // 邮件内容
    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: 'ryanrc230107@gmail.com',
      subject: `Portfolio Contact Form - Message from ${firstName} ${lastName}`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
          <div style="background-color: #0a0a0a; color: white; padding: 20px; border-radius: 10px;">
            <h2 style="color: #00D9FF; margin-bottom: 20px;">New Contact Form Submission</h2>
            
            <div style="background-color: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
              <h3 style="color: #00D9FF; margin-top: 0;">Contact Information:</h3>
              <p><strong>Name:</strong> ${firstName} ${lastName}</p>
              <p><strong>Email:</strong> ${emailId}</p>
              ${mobNo ? `<p><strong>Phone:</strong> ${mobNo}</p>` : ''}
            </div>
            
            <div style="background-color: #1a1a1a; padding: 20px; border-radius: 8px;">
              <h3 style="color: #00D9FF; margin-top: 0;">Message:</h3>
              <p style="line-height: 1.6; white-space: pre-wrap;">${message}</p>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background-color: #2a2a2a; border-radius: 8px; text-align: center;">
              <p style="margin: 0; color: #00D9FF; font-size: 14px;">
                This message was sent from your portfolio contact form
              </p>
            </div>
          </div>
        </div>
      `,
      // 回复地址设置为联系人的邮箱
      replyTo: emailId,
    };

    console.log('Sending email...');

    // 发送邮件
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent successfully:', info.messageId);

    return NextResponse.json(
      { message: 'Email sent successfully', messageId: info.messageId },
      { status: 200 }
    );

  } catch (error) {
    console.error('Error sending email:', error);
    
    // 返回更详细的错误信息
    let errorMessage = 'Failed to send email';
    if (error instanceof Error) {
      errorMessage = error.message;
    }
    
    return NextResponse.json(
      { error: errorMessage },
      { status: 500 }
    );
  }
}