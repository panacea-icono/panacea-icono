#!/usr/bin/env python3
"""
🏥 PANACEA ICONO S.A. - Gestor de Bots de Telegram
Sistema centralizado para gestionar todos los bots del ecosistema
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TelegramBot:
    """Estructura para un bot de Telegram"""
    name: str
    username: str
    token: str
    description: str
    category: str
    status: str = "inactive"
    last_activity: Optional[datetime] = None
    error_count: int = 0

class PanaceaTelegramManager:
    """Gestor centralizado de bots de Telegram para Panacea Icono S.A."""
    
    def __init__(self):
        self.bots: Dict[str, TelegramBot] = {}
        self.base_url = "https://api.telegram.org/bot"
        self._load_bots_from_env()
    
    def _load_bots_from_env(self):
        """Cargar bots desde variables de entorno"""
        bot_tokens = {
            # Bots médicos principales
            "ALINA": ("ALINA_KUCHITV_BOT", "7736162376:AAFY-oLaHuOd3VEUlPa1fJjAnCLeow1APto", "Bot de consultas médicas generales", "medical"),
            "Anastasia": ("Anastasia_panacea_bot", "8113198067:AAEevfvj5k_aAzr-4fbgjxpGbpzq_PCT-Uk", "Asistente de cirugía plástica", "medical"),
            "Dr_Lalo": ("Dr_Lalo_bot", "8144751411:AAGGRYXb9As2Kd1tJEMaVQ5qWjWfJm1WdIo", "Dr. Lalo - Consultas especializadas", "medical"),
            "DrAquiles": ("DRAQUILES_bot", "7552009866:AAEPQrwbA4BJ6BgFkzNhUzIiz7BRLh4deuM", "Dr. Aquiles - Medicina estética", "medical"),
            "plastic_surgeon": ("vaser_plastic_surgeon_bot", "7735301496:AAFhWecy29jjPIP-QLwMBHyt7W-b8MTOhX4", "Cirujano plástico especializado", "medical"),
            "Dra_Liliana": ("Dra_Liliana_bot", "7934673190:AAFMO27pg1uYyE3jor1x6O2iGSCb7RDhKWY", "Dra. Liliana - Ginecología estética", "medical"),
            "face_surgery": ("face_surgery_bot", "7835937499:AAHahj4IAghOuWRmeusyIw7RhZGWN9G23yg", "Cirugía facial especializada", "medical"),
            "vaser_plastic": ("vaser_plastic_surgeon_bot", "7164860773:AAFw0lpdE0-mby5IMQnoZFRb74giZ4zr3r0", "Técnicas VASER especializadas", "medical"),
            
            # Bots de tokens y pagos
            "Panas": ("Panas_token_bot", "7828486767:AAHQQ98T2orrJfDOJEyZ1_8HSvSuJ08bJzA", "Bot oficial del token PANAS", "crypto"),
            "Vaser_token": ("CLINICA_VASER_BOT", "7622504424:AAGQjIbXs3fs9ITUiDFBuzNG5PmJHb4Sxao", "Token de la clínica VASER", "crypto"),
            "Liposuccion": ("Liposuccion_bot", "8187502572:AAFn2bEOOqDipeDWTnszjyWyiBUUBsofMis", "Pagos para liposucción", "crypto"),
            
            # Bots de entretenimiento y medios
            "CONDE_MORMIX": ("CONDE_MORMIX_bot", "7958735108:AAEnPCdiF3_NsfgAO1ZQJK-pVVv-OzgT31k", "Entretenimiento y contenido", "entertainment"),
            "Poci": ("Pontificia_bot", "7813930559:AAEguGKbO3WlWlt1BenLkBrmATpuCUtfxZw", "Contenido pontificio", "entertainment"),
            "la_chunchuna": ("la_chunchuna_bot", "7584900206:AAFvBWakpuvo7kLxUcFnbzkpCTDj5GEhlb0", "Entretenimiento local", "entertainment"),
            "IVANA": ("IVANA_TV_BOT", "7226803911:AAEBZa5DN7ppTGqL8WuicvH1Zpucoj0ju18", "Canal de TV de Ivana", "media"),
            "Catolica": ("Catolica_boliviana_bot", "7837429936:AAHAiTyZncM3V7ysqwo7Fs0NV2nOi-iE4g", "Contenido católico", "religious"),
            "DR_DELA_TV": ("dR_tv_BOT", "8151444219:AAHe28kkVynPKUn3o75jSVBUMUdAMoLNFHQ", "Dr. de la TV - Canal médico", "media"),
            "Jabancho": ("Jabancho_bot", "7715564591:AAGjqzaIQiR4JVov9ipJtnvdGB5TOzcysH4", "Entretenimiento", "entertainment"),
            "monica": ("monica_vaser_bot", "7164860773:AAFw0lpdE0-mby5IMQnoZFRb74giZ4zr3r0", "Monica VASER", "medical"),
            "Alejandra": ("Alejandra_MD_bot", "7461930898:AAHZjFntuq0IE4mIUKE3kOF7H87AJk8lYns", "Dra. Alejandra MD", "medical"),
            "sophie": ("Sophie_DrTV_bot", "8046291328:AAFfYZ4JexrnNsqkgrGoLUHs11T1IGLoWJ8", "Sophie DrTV", "media"),
            "SOCIEDAD": ("Sociedad_bot", "7653405457:AAH2-RqwWOr4z0FSb7ua2B0uWfFKcfK3ox4", "Sociedad médica", "medical"),
            "Kuchiuya": ("Kuchiuya_bot", "7630335998:AAGhGk25gfHWCxceMKGVly43WH7-W0ufC88", "Kuchiuya - Personal", "personal"),
            "dr_tapia": ("dr_tapia_bot", "8077214672:AAGn7tU3kcC1fMAFmA6HSQTZSCBG-3i9UPE", "Dr. Tapia - CEO", "medical"),
            "Lalo": ("Lalabot007_bot", "7587868575:AAHLc_SlrzTae3Ae6u-pgMvScFSpuzmW4yM", "Lalo 007", "personal"),
            "Guerita": ("La_guerita_bot", "7267919371:AAFLVcOeoffUAv2S0_Dq13L1SNmwTAWk", "La Guerita", "personal"),
            "Joselin": ("Joselin_2025_bot", "7892244472:AAFeXHfXwHJuVRg2tKs-V2xMS8JihKOaIv4", "Joselin 2025", "personal"),
            "ana_maria": ("face_surgery_bot", "7835937499:AAHahj4IAghOuWRmeusyIw7RhZGWN9G23yg", "Ana Maria - Cirugía facial", "medical"),
            "Ingenio": ("Universidad_bot", "8187502572:AAFn2bEOOqDipeDWTnszjyWyiBUUBsofMis", "Universidad", "education"),
            "Catalina": ("Universidad_Catolica_bot", "7523398376:AAGhS6je5tlg0CKMW6rMGwwaBSJiJm5bpY0", "Universidad Católica", "education"),
            "Analia": ("Boliviana_bot", "7155901429:AAFTyNZ2VQlufM8gR-TQCiMPD1rsE1qqOAE", "Analia Boliviana", "personal"),
        }
        
        for name, (username, token, description, category) in bot_tokens.items():
            self.bots[name] = TelegramBot(
                name=name,
                username=username,
                token=token,
                description=description,
                category=category
            )
    
    async def check_bot_health(self, bot_name: str) -> Dict[str, Any]:
        """Verificar el estado de un bot específico"""
        if bot_name not in self.bots:
            return {"error": f"Bot {bot_name} no encontrado"}
        
        bot = self.bots[bot_name]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}{bot.token}/getMe")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        bot.status = "active"
                        bot.last_activity = datetime.now()
                        bot.error_count = 0
                        return {
                            "status": "active",
                            "bot_info": data["result"],
                            "last_check": datetime.now().isoformat()
                        }
                    else:
                        bot.status = "error"
                        bot.error_count += 1
                        return {"status": "error", "message": data.get("description", "Unknown error")}
                else:
                    bot.status = "error"
                    bot.error_count += 1
                    return {"status": "error", "message": f"HTTP {response.status_code}"}
        except Exception as e:
            bot.status = "error"
            bot.error_count += 1
            return {"status": "error", "message": str(e)}
    
    async def check_all_bots_health(self) -> Dict[str, Any]:
        """Verificar el estado de todos los bots"""
        results = {}
        for bot_name in self.bots:
            results[bot_name] = await self.check_bot_health(bot_name)
        return results
    
    async def send_message(self, bot_name: str, chat_id: str, message: str) -> Dict[str, Any]:
        """Enviar mensaje a través de un bot específico"""
        if bot_name not in self.bots:
            return {"error": f"Bot {bot_name} no encontrado"}
        
        bot = self.bots[bot_name]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}{bot.token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"🏥 **Panacea Icono S.A.**\n\n{message}",
                        "parse_mode": "Markdown"
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ok"):
                        return {"status": "success", "message_id": data["result"]["message_id"]}
                    else:
                        return {"status": "error", "message": data.get("description")}
                else:
                    return {"status": "error", "message": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_bots_by_category(self, category: str) -> List[TelegramBot]:
        """Obtener bots por categoría"""
        return [bot for bot in self.bots.values() if bot.category == category]
    
    def get_bot_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de los bots"""
        total_bots = len(self.bots)
        active_bots = len([bot for bot in self.bots.values() if bot.status == "active"])
        error_bots = len([bot for bot in self.bots.values() if bot.status == "error"])
        
        categories = {}
        for bot in self.bots.values():
            if bot.category not in categories:
                categories[bot.category] = 0
            categories[bot.category] += 1
        
        return {
            "total_bots": total_bots,
            "active_bots": active_bots,
            "error_bots": error_bots,
            "inactive_bots": total_bots - active_bots - error_bots,
            "categories": categories,
            "last_update": datetime.now().isoformat()
        }

# Instancia global del gestor
telegram_manager = PanaceaTelegramManager()

async def main():
    """Función principal para testing"""
    print("🏥 PANACEA ICONO S.A. - Gestor de Bots de Telegram")
    print("=" * 50)
    
    # Mostrar estadísticas
    stats = telegram_manager.get_bot_stats()
    print(f"Total de bots: {stats['total_bots']}")
    print(f"Bots activos: {stats['active_bots']}")
    print(f"Bots con error: {stats['error_bots']}")
    print(f"Categorías: {stats['categories']}")
    
    # Verificar salud de todos los bots
    print("\n🔍 Verificando salud de los bots...")
    health_results = await telegram_manager.check_all_bots_health()
    
    for bot_name, result in health_results.items():
        status_emoji = "✅" if result.get("status") == "active" else "❌"
        print(f"{status_emoji} {bot_name}: {result.get('status', 'unknown')}")

if __name__ == "__main__":
    asyncio.run(main())
