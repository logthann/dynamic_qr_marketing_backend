from typing import Optional
import datetime

from sqlalchemy import BigInteger, CheckConstraint, Date, ForeignKeyConstraint, Index, Integer, JSON, String, TIMESTAMP, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.db.session import Base

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("(`role` in (_utf8mb4'admin',_utf8mb4'agency',_utf8mb4'user'))", name='users_chk_1'),
        Index('email', 'email', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[Optional[str]] = mapped_column(String(50))
    subscription_plan: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    campaigns: Mapped[list['Campaigns']] = relationship('Campaigns', back_populates='user')
    userintegrations: Mapped[list['Userintegrations']] = relationship('Userintegrations', back_populates='user')
    qrcodes: Mapped[list['Qrcodes']] = relationship('Qrcodes', back_populates='user')


class Campaigns(Base):
    __tablename__ = 'campaigns'
    __table_args__ = (
        CheckConstraint("(`status` in (_utf8mb4'active',_utf8mb4'paused',_utf8mb4'completed',_utf8mb4'draft'))", name='campaigns_chk_1'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='campaigns_ibfk_1'),
        Index('idx_campaigns_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ga_measurement_id: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'active'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='campaigns')
    qrcodes: Mapped[list['Qrcodes']] = relationship('Qrcodes', back_populates='campaign')


class Userintegrations(Base):
    __tablename__ = 'userintegrations'
    __table_args__ = (
        CheckConstraint("(`provider_name` in (_utf8mb4'google_calendar',_utf8mb4'google_analytics'))", name='userintegrations_chk_1'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='userintegrations_ibfk_1'),
        Index('unique_user_provider', 'user_id', 'provider_name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_name: Mapped[str] = mapped_column(String(50), nullable=False)
    access_token: Mapped[Optional[str]] = mapped_column(Text)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text)
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='userintegrations')


class Qrcodes(Base):
    __tablename__ = 'qrcodes'
    __table_args__ = (
        CheckConstraint("(`qr_type` in (_utf8mb4'url',_utf8mb4'event',_utf8mb4'vcard',_utf8mb4'app'))", name='qrcodes_chk_1'),
        CheckConstraint("(`status` in (_utf8mb4'active',_utf8mb4'paused'))", name='qrcodes_chk_2'),
        ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='SET NULL', name='qrcodes_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='qrcodes_ibfk_1'),
        Index('idx_qrcodes_campaign_id', 'campaign_id'),
        Index('idx_qrcodes_user_id', 'user_id'),
        Index('short_code', 'short_code', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_code: Mapped[str] = mapped_column(String(50), nullable=False)
    destination_url: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_id: Mapped[Optional[int]] = mapped_column(Integer)
    qr_type: Mapped[Optional[str]] = mapped_column(String(50))
    design_config: Mapped[Optional[dict]] = mapped_column(JSON)
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'active'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    campaign: Mapped[Optional['Campaigns']] = relationship('Campaigns', back_populates='qrcodes')
    user: Mapped['Users'] = relationship('Users', back_populates='qrcodes')
    dailyanalyticssummary: Mapped[list['Dailyanalyticssummary']] = relationship('Dailyanalyticssummary', back_populates='qr')
    qreventdetails: Mapped[list['Qreventdetails']] = relationship('Qreventdetails', back_populates='qr')
    scanlogs: Mapped[list['Scanlogs']] = relationship('Scanlogs', back_populates='qr')


class Dailyanalyticssummary(Base):
    __tablename__ = 'dailyanalyticssummary'
    __table_args__ = (
        ForeignKeyConstraint(['qr_id'], ['qrcodes.id'], ondelete='CASCADE', name='dailyanalyticssummary_ibfk_1'),
        Index('idx_daily_summary_qr_date', 'qr_id', 'summary_date'),
        Index('unique_qr_date', 'qr_id', 'summary_date', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    qr_id: Mapped[int] = mapped_column(Integer, nullable=False)
    summary_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    total_scans: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))
    unique_visitors: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))

    qr: Mapped['Qrcodes'] = relationship('Qrcodes', back_populates='dailyanalyticssummary')


class Qreventdetails(Base):
    __tablename__ = 'qreventdetails'
    __table_args__ = (
        ForeignKeyConstraint(['qr_id'], ['qrcodes.id'], ondelete='CASCADE', name='qreventdetails_ibfk_1'),
        Index('qr_id', 'qr_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    qr_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_datetime: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    end_datetime: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    google_event_id: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    qr: Mapped['Qrcodes'] = relationship('Qrcodes', back_populates='qreventdetails')


class Scanlogs(Base):
    __tablename__ = 'scanlogs'
    __table_args__ = (
        ForeignKeyConstraint(['qr_id'], ['qrcodes.id'], ondelete='CASCADE', name='scanlogs_ibfk_1'),
        Index('idx_scanlogs_qr_id_scanned_at', 'qr_id', 'scanned_at')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    qr_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scanned_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    device_type: Mapped[Optional[str]] = mapped_column(String(50))
    os: Mapped[Optional[str]] = mapped_column(String(50))
    browser: Mapped[Optional[str]] = mapped_column(String(50))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    referer: Mapped[Optional[str]] = mapped_column(Text)

    qr: Mapped['Qrcodes'] = relationship('Qrcodes', back_populates='scanlogs')
