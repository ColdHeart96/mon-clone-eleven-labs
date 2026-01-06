from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from kokoro import KPipeline
import soundfile as sf
import io
import numpy as np
import logging # Pour le système de logs
from fastapi.middleware.cors import CORSMiddleware

# 1. Configuration du Système de Journalisation (Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("tts-api")

app = FastAPI(title="Kokoro TTS API Professional")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Autorise tout le monde (pour le dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle
logger.info("Chargement du modèle Kokoro v0.19 sur CPU...")
pipeline = KPipeline(lang_code='a', device='cpu')
logger.info("Modèle chargé avec succès.")

# 2. Modèle de données avec contrôle de longueur (Contrôle durée texte)
class TTSRequest(BaseModel):
    # On limite à 500 caractères pour protéger le CPU
    text: str = Field(..., max_length=500, description="Le texte à convertir en audio")
    voice: str = "af_heart"

@app.get("/")
def read_root():
    return {"status": "online", "model": "Kokoro v0.19"}

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    # Log de la requête
    logger.info(f"Requête reçue pour la voix {request.voice}. Longueur texte: {len(request.text)}")
    
    try:
        # Génération
        generator = pipeline(request.text, voice=request.voice, speed=1.0)
        
        audio_segments = [audio for _, _, audio in generator if audio is not None]

        if not audio_segments:
            logger.error("Échec de la génération : aucun segment audio produit.")
            raise HTTPException(status_code=500, detail="Erreur interne : aucun audio généré.")

        # Fusion
        final_audio = np.concatenate(audio_segments)

        # Création du WAV
        buffer = io.BytesIO()
        sf.write(buffer, final_audio, 24000, format='WAV')
        audio_bytes = buffer.getvalue()

        # Log de succès
        logger.info("Synthèse vocale réussie. Envoi du fichier.")

        # Réponse standardisée avec headers
        headers = {'Content-Disposition': 'attachment; filename="speech.wav"'}
        return Response(content=audio_bytes, media_type="audio/wav", headers=headers)

    except Exception as e:
        # Gestion robuste des erreurs
        logger.error(f"Erreur critique lors de la synthèse : {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={"error": "Erreur lors du traitement TTS", "details": str(e)}
        )