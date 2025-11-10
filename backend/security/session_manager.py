"""
Session Manager

Manages chat sessions with security features including IP validation,
session expiry, and request limits.
"""

import uuid
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


class SessionManager:
    """
    Session manager with security features.
    
    Features:
    - IP address validation (prevents session hijacking)
    - Session expiry (2 hours)
    - Request count limits (max 100 per session)
    - Active session limits (max 50 per IP)
    """
    
    def __init__(self, session_expiry_hours: int = 2, max_requests_per_session: int = 100, max_sessions_per_ip: int = 50):
        """
        Initialize session manager.
        
        Args:
            session_expiry_hours: Hours until session expires (default: 2)
            max_requests_per_session: Maximum requests per session (default: 100)
            max_sessions_per_ip: Maximum active sessions per IP (default: 50)
        """
        self.session_expiry_hours = session_expiry_hours
        self.max_requests_per_session = max_requests_per_session
        self.max_sessions_per_ip = max_sessions_per_ip
        
        # Session storage: session_id -> session_data
        self._sessions: Dict[str, dict] = {}
        
        # IP to session IDs mapping
        self._ip_sessions: Dict[str, list] = {}
    
    def create_session(self, ip_address: str, category: str) -> Tuple[str, str]:
        """
        Create a new session with security token.
        
        Args:
            ip_address: Client IP address
            category: Business category
            
        Returns:
            Tuple of (session_id, security_token)
        """
        # Clean up expired sessions first
        self.cleanup_expired_sessions()
        
        # Check session limit per IP
        ip_sessions = self._ip_sessions.get(ip_address, [])
        active_sessions = [s for s in ip_sessions if self._is_session_active(s)]
        
        if len(active_sessions) >= self.max_sessions_per_ip:
            raise ValueError(f"Maximum {self.max_sessions_per_ip} active sessions per IP address")
        
        # Generate session ID and security token
        session_id = str(uuid.uuid4())
        security_token = secrets.token_urlsafe(32)
        
        # Create session data
        session_data = {
            'session_id': session_id,
            'security_token': security_token,
            'ip_address': ip_address,
            'category': category,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=self.session_expiry_hours),
            'request_count': 0,
            'answers': {},
            'conversation': [],
            'current_question_id': None
        }
        
        # Store session
        self._sessions[session_id] = session_data
        
        # Track IP sessions
        if ip_address not in self._ip_sessions:
            self._ip_sessions[ip_address] = []
        self._ip_sessions[ip_address].append(session_id)
        
        return session_id, security_token
    
    def validate_session(self, session_id: str, ip_address: str, security_token: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Validate session and check IP address match.
        
        Args:
            session_id: Session ID to validate
            ip_address: Current client IP address
            security_token: Optional security token for additional validation
            
        Returns:
            Tuple of (is_valid, error_message, session_data)
        """
        # Check if session exists
        if session_id not in self._sessions:
            return False, "Session not found", None
        
        session = self._sessions[session_id]
        
        # Check if session expired
        if datetime.now() >= session['expires_at']:
            self._remove_session(session_id)
            return False, "Session expired", None
        
        # Check IP address match (prevent session hijacking)
        if session['ip_address'] != ip_address:
            return False, "Session IP address mismatch (possible hijacking attempt)", None
        
        # Check security token if provided
        if security_token and session.get('security_token') != security_token:
            return False, "Invalid security token", None
        
        # Check request count limit
        if session['request_count'] >= self.max_requests_per_session:
            return False, f"Maximum {self.max_requests_per_session} requests per session exceeded", None
        
        return True, None, session
    
    def increment_request_count(self, session_id: str):
        """Increment request count for session."""
        if session_id in self._sessions:
            self._sessions[session_id]['request_count'] += 1
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data if valid."""
        if session_id not in self._sessions:
            return None
        
        session = self._sessions[session_id]
        
        # Check if expired
        if datetime.now() >= session['expires_at']:
            self._remove_session(session_id)
            return None
        
        return session
    
    def update_session(self, session_id: str, updates: dict):
        """Update session data."""
        if session_id in self._sessions:
            self._sessions[session_id].update(updates)
    
    def _is_session_active(self, session_id: str) -> bool:
        """Check if session is still active (not expired)."""
        if session_id not in self._sessions:
            return False
        
        session = self._sessions[session_id]
        return datetime.now() < session['expires_at']
    
    def _remove_session(self, session_id: str):
        """Remove session and clean up IP tracking."""
        if session_id in self._sessions:
            ip_address = self._sessions[session_id]['ip_address']
            del self._sessions[session_id]
            
            # Remove from IP tracking
            if ip_address in self._ip_sessions:
                self._ip_sessions[ip_address] = [
                    s for s in self._ip_sessions[ip_address] if s != session_id
                ]
                if not self._ip_sessions[ip_address]:
                    del self._ip_sessions[ip_address]
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions."""
        now = datetime.now()
        expired = [
            session_id for session_id, session in self._sessions.items()
            if now >= session['expires_at']
        ]
        
        for session_id in expired:
            self._remove_session(session_id)
    
    def get_active_sessions_count(self, ip_address: str) -> int:
        """Get count of active sessions for IP address."""
        ip_sessions = self._ip_sessions.get(ip_address, [])
        return len([s for s in ip_sessions if self._is_session_active(s)])
    
    def clear_sessions_for_ip(self, ip_address: str):
        """Clear all sessions for a specific IP address."""
        if ip_address in self._ip_sessions:
            session_ids = self._ip_sessions[ip_address].copy()
            for session_id in session_ids:
                if session_id in self._sessions:
                    del self._sessions[session_id]
            del self._ip_sessions[ip_address]
    
    def clear_all_sessions(self):
        """Clear all sessions (useful for testing or reset)."""
        self._sessions.clear()
        self._ip_sessions.clear()

