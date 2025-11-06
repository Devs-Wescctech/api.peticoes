-- Extensões PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- Para busca full-text

-- =====================================================
-- TABELA: users
-- =====================================================
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
  phone VARCHAR(50),
  avatar_url TEXT,
  preferences JSONB DEFAULT '{ "email_notifications": true, "weekly_report": true }',
  email_verified BOOLEAN DEFAULT FALSE,
  reset_token VARCHAR(255),
  reset_token_expires TIMESTAMP,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- =====================================================
-- TABELA: petitions
-- =====================================================
CREATE TABLE petitions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title VARCHAR(500) NOT NULL,
  description TEXT NOT NULL,
  banner_url TEXT,
  logo_url TEXT,
  primary_color VARCHAR(7) DEFAULT '#6366f1',
  share_text TEXT,
  goal INTEGER NOT NULL CHECK (goal > 0),
  status VARCHAR(50) DEFAULT 'rascunho' CHECK (status IN ('rascunho', 'publicada', 'pausada', 'concluida')),
  slug VARCHAR(255) UNIQUE,
  collect_phone BOOLEAN DEFAULT FALSE,
  collect_city BOOLEAN DEFAULT TRUE,
  collect_state BOOLEAN DEFAULT FALSE,
  collect_cpf BOOLEAN DEFAULT FALSE,
  collect_comment BOOLEAN DEFAULT TRUE,
  views_count INTEGER DEFAULT 0,
  shares_count INTEGER DEFAULT 0,
  created_by VARCHAR(255),
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_petitions_status ON petitions(status);
CREATE INDEX idx_petitions_slug ON petitions(slug);
CREATE INDEX idx_petitions_created_by ON petitions(created_by);
CREATE INDEX idx_petitions_title_trgm ON petitions USING gin(title gin_trgm_ops);

-- =====================================================
-- TABELA: signatures
-- =====================================================
CREATE TABLE signatures (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  petition_id UUID REFERENCES petitions(id) ON DELETE CASCADE NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  city VARCHAR(255),
  state VARCHAR(50),
  cpf VARCHAR(14),
  comment TEXT,
  ip_address INET,
  user_agent TEXT,
  created_by VARCHAR(255),
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW(),
  UNIQUE(petition_id, email)
);
CREATE INDEX idx_signatures_petition_id ON signatures(petition_id);
CREATE INDEX idx_signatures_email ON signatures(email);
CREATE INDEX idx_signatures_city ON signatures(city);
CREATE INDEX idx_signatures_state ON signatures(state);
CREATE INDEX idx_signatures_created_date ON signatures(created_date DESC);

-- =====================================================
-- TABELA: campaigns
-- =====================================================
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL CHECK (type IN ('whatsapp', 'email')),
  status VARCHAR(50) DEFAULT 'rascunho' CHECK (status IN ('rascunho', 'agendada', 'enviando', 'concluida', 'pausada')),
  petition_id UUID REFERENCES petitions(id) ON DELETE SET NULL,
  target_petitions TEXT[],
  target_filters JSONB DEFAULT '{}',
  message TEXT NOT NULL,
  subject VARCHAR(500),
  sender_email VARCHAR(255),
  sender_name VARCHAR(255),
  scheduled_date TIMESTAMP,
  sent_count INTEGER DEFAULT 0,
  success_count INTEGER DEFAULT 0,
  failed_count INTEGER DEFAULT 0,
  total_recipients INTEGER DEFAULT 0,
  api_token TEXT,
  delay_seconds INTEGER DEFAULT 3 CHECK (delay_seconds >= 1),
  messages_per_hour INTEGER DEFAULT 20 CHECK (messages_per_hour > 0),
  avoid_night_hours BOOLEAN DEFAULT TRUE,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_by VARCHAR(255),
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_campaigns_type ON campaigns(type);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_petition_id ON campaigns(petition_id);
CREATE INDEX idx_campaigns_scheduled_date ON campaigns(scheduled_date);

-- =====================================================
-- TABELA: campaign_logs
-- =====================================================
CREATE TABLE campaign_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE NOT NULL,
  recipient_name VARCHAR(255) NOT NULL,
  recipient_contact VARCHAR(255) NOT NULL,
  status VARCHAR(50) NOT NULL CHECK (status IN ('success', 'error', 'pending')),
  response_status VARCHAR(10),
  response_body TEXT,
  error_message TEXT,
  sent_at TIMESTAMP DEFAULT NOW(),
  created_by VARCHAR(255),
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_campaign_logs_campaign_id ON campaign_logs(campaign_id);
CREATE INDEX idx_campaign_logs_status ON campaign_logs(status);
CREATE INDEX idx_campaign_logs_sent_at ON campaign_logs(sent_at DESC);

-- =====================================================
-- TABELA: linkbio_pages
-- =====================================================
CREATE TABLE linkbio_pages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  avatar_url TEXT,
  background_color VARCHAR(7) DEFAULT '#6366f1',
  status VARCHAR(50) DEFAULT 'rascunho' CHECK (status IN ('rascunho', 'publicada')),
  petition_ids TEXT[],
  views_count INTEGER DEFAULT 0,
  clicks_count INTEGER DEFAULT 0,
  created_by VARCHAR(255),
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_linkbio_pages_slug ON linkbio_pages(slug);
CREATE INDEX idx_linkbio_pages_status ON linkbio_pages(status);

-- =====================================================
-- TABELA: message_templates
-- =====================================================
CREATE TABLE message_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL CHECK (type IN ('whatsapp', 'email')),
  subject VARCHAR(500),
  content TEXT NOT NULL,
  is_default BOOLEAN DEFAULT FALSE,
  thumbnail_url TEXT,
  usage_count INTEGER DEFAULT 0,
  created_by VARCHAR(255),
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_message_templates_type ON message_templates(type);
CREATE INDEX idx_message_templates_is_default ON message_templates(is_default);

-- =====================================================
-- TRIGGERS: updated_date automático
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_date() RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_date = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_date BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_date();
CREATE TRIGGER update_petitions_updated_date BEFORE UPDATE ON petitions FOR EACH ROW EXECUTE FUNCTION update_updated_date();
CREATE TRIGGER update_signatures_updated_date BEFORE UPDATE ON signatures FOR EACH ROW EXECUTE FUNCTION update_updated_date();
CREATE TRIGGER update_campaigns_updated_date BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_date();
CREATE TRIGGER update_linkbio_pages_updated_date BEFORE UPDATE ON linkbio_pages FOR EACH ROW EXECUTE FUNCTION update_updated_date();
CREATE TRIGGER update_message_templates_updated_date BEFORE UPDATE ON message_templates FOR EACH ROW EXECUTE FUNCTION update_updated_date();

-- =====================================================
-- VIEWS ÚTEIS
-- =====================================================
-- View: Estatísticas de Petições
CREATE OR REPLACE VIEW petition_stats AS
SELECT p.id, p.title, p.goal, p.status,
       COUNT(DISTINCT s.id) as signature_count,
       ROUND((COUNT(DISTINCT s.id)::NUMERIC / p.goal) * 100, 2) as progress_percentage,
       p.views_count, p.shares_count, p.created_date
  FROM petitions p
  LEFT JOIN signatures s ON p.id = s.petition_id
 GROUP BY p.id;

-- View: Performance de Campanhas
CREATE OR REPLACE VIEW campaign_performance AS
SELECT c.id, c.name, c.type, c.status, c.sent_count, c.success_count, c.failed_count,
       CASE WHEN c.sent_count > 0 THEN ROUND((c.success_count::NUMERIC / c.sent_count) * 100, 2) ELSE 0 END as success_rate,
       c.created_date
  FROM campaigns c;

-- =====================================================
-- DADOS INICIAIS (OPCIONAL)
-- =====================================================
-- Template padrão de WhatsApp
INSERT INTO message_templates (name, type, content, is_default)
VALUES ('Boas-vindas WhatsApp', 'whatsapp', 'Olá {name}! 👋 Obrigado por assinar nossa petição "{petition_title}"! Sua assinatura faz toda a diferença. Juntos somos mais fortes! Compartilhe: {petition_link}', true);

-- Template padrão de Email
INSERT INTO message_templates (name, type, subject, content, is_default)
VALUES ('Boas-vindas Email', 'email', 'Obrigado por assinar!',
        '<html> <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;"> <h2 style="color: #6366f1;">Obrigado, {name}!</h2> <p>Sua assinatura na petição <strong>{petition_title}</strong> foi confirmada!</p> <p>Cada voz conta e sua participação é fundamental para alcançarmos nossa meta.</p> <a href__="{petition_link}" style="display: inline-block; background: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-top: 20px;"> Ver Petição </a> <p style="margin-top: 30px; font-size: 12px; color: #666;"> Compartilhe com seus amigos e ajude a causa! </p> </body> </html>',
        true);
