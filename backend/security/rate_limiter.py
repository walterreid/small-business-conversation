"""
Rate Limiter

Implements rate limiting with blocking for violations.
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict
from collections import defaultdict


class RateLimiter:
    """
    Rate limiter with blocking mechanism.
    
    Tracks requests per identifier and blocks after violations.
    """
    
    def __init__(self):
        # Request timestamps per identifier
        self._request_history: Dict[str, list] = defaultdict(list)
        
        # Blocked identifiers with unblock time
        self._blocked: Dict[str, datetime] = {}
        
        # Default limits
        self.default_max_requests = 10
        self.default_window_seconds = 60
        self.default_block_duration_seconds = 300  # 5 minutes
    
    def is_allowed(
        self, 
        identifier: str,
        max_requests: Optional[int] = None,
        window_seconds: Optional[int] = None,
        block_duration_seconds: Optional[int] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if request is allowed for identifier.
        
        Args:
            identifier: Unique identifier (IP address, session ID, etc.)
            max_requests: Maximum requests allowed (default: 10)
            window_seconds: Time window in seconds (default: 60)
            block_duration_seconds: Block duration after violation (default: 300)
        
        Returns:
            Tuple of (is_allowed, error_message)
        """
        now = datetime.now()
        
        # Use defaults if not specified
        max_requests = max_requests or self.default_max_requests
        window_seconds = window_seconds or self.default_window_seconds
        block_duration_seconds = block_duration_seconds or self.default_block_duration_seconds
        
        # Check if identifier is currently blocked
        if identifier in self._blocked:
            unblock_time = self._blocked[identifier]
            if now < unblock_time:
                remaining = (unblock_time - now).total_seconds()
                return False, f"Rate limit exceeded. Blocked for {int(remaining)} more seconds."
            else:
                # Block expired, remove it
                del self._blocked[identifier]
        
        # Get request history for this identifier
        requests = self._request_history[identifier]
        window_start = now - timedelta(seconds=window_seconds)
        
        # Remove old requests outside window
        requests[:] = [req_time for req_time in requests if req_time > window_start]
        
        # Check if limit exceeded
        if len(requests) >= max_requests:
            # Block the identifier
            block_until = now + timedelta(seconds=block_duration_seconds)
            self._blocked[identifier] = block_until
            return False, f"Rate limit exceeded. Blocked for {block_duration_seconds} seconds."
        
        # Add current request
        requests.append(now)
        
        return True, None
    
    def clear_old_data(self, max_age_seconds: int = 3600):
        """
        Clean up old request history and expired blocks.
        
        Args:
            max_age_seconds: Maximum age for request history (default: 1 hour)
        """
        now = datetime.now()
        cutoff = now - timedelta(seconds=max_age_seconds)
        
        # Clean up old request history
        for identifier in list(self._request_history.keys()):
            requests = self._request_history[identifier]
            requests[:] = [req_time for req_time in requests if req_time > cutoff]
            
            # Remove empty histories
            if not requests:
                del self._request_history[identifier]
        
        # Clean up expired blocks
        for identifier in list(self._blocked.keys()):
            if now >= self._blocked[identifier]:
                del self._blocked[identifier]
    
    def get_status(self, identifier: str) -> dict:
        """
        Get rate limit status for identifier.
        
        Args:
            identifier: Identifier to check
            
        Returns:
            Dictionary with status information
        """
        now = datetime.now()
        
        # Check if blocked
        is_blocked = identifier in self._blocked and now < self._blocked[identifier]
        block_until = self._blocked.get(identifier) if is_blocked else None
        
        # Count recent requests
        requests = self._request_history.get(identifier, [])
        window_start = now - timedelta(seconds=60)
        recent_requests = [r for r in requests if r > window_start]
        
        return {
            'is_blocked': is_blocked,
            'block_until': block_until.isoformat() if block_until else None,
            'recent_requests_count': len(recent_requests),
            'total_requests_count': len(requests)
        }

