from ..exceptions import ValidationError


class RequestValidator:

    def __init__(self, config):
        self.config = config
        
        
    def _validate(self):
        
        if not self.config.api_key:
            raise ValidationError("API key is required")

        if not self.config.app_id:
            raise ValidationError("App ID is required")

        if not self.config.app_secret:
            raise ValidationError("App secret is required")

        if not self.config.app_platform:
            raise ValidationError("App platform is required")

        if not self.config.app_identifier:
            raise ValidationError("App identifier is required")
        

    def build_headers(self):
        
        self._validate()

        headers = {
            "X-API-Key": self.config.api_key,
            "X-App-ID": self.config.app_id,
            "X-App-Secret": self.config.app_secret,
            "X-App-Platform": self.config.app_platform,
            "X-App-Identifier": self.config.app_identifier,
            
        }

        if self.config.app_name:
            headers["X-App-Name"] = self.config.app_name

        if self.config.domain:
            headers["X-Domain"] = self.config.domain

        return headers