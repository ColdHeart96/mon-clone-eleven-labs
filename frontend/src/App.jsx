import { useState } from 'react'
import axios from 'axios'

function App() {
  const [text, setText] = useState('')      // Stocke le texte saisi
  const [loading, setLoading] = useState(false) // Savoir si l'IA travaille
  const [audioUrl, setAudioUrl] = useState(null) // Stocke le lien de l'audio généré

  const generateTTS = async () => {
    if (!text) return alert("Écris quelque chose !")
    
    setLoading(true)
    try {
      // On appelle ton API FastAPI
      // responseType: 'blob' est CRUCIAL pour recevoir un fichier audio
      const response = await axios.post('http://127.0.0.1:8000/tts', 
        { text: text, voice: "af_heart" },
        { responseType: 'blob' } 
      )

      // On transforme les données binaires reçues en un lien utilisable par le navigateur
      const url = window.URL.createObjectURL(new Blob([response.data]))
      setAudioUrl(url)
    } catch (error) {
      console.error("Erreur lors de la génération:", error)
      alert("Erreur serveur")
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '40px', textAlign: 'center', fontFamily: 'Arial' }}>
      <h1>Mon Clone Eleven Labs</h1>
      
      <textarea 
        placeholder="Entrez votre texte ici..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ width: '80%', height: '100px', marginBottom: '20px', padding: '10px' }}
      />
      
      <br />
      
      <button 
        onClick={generateTTS} 
        disabled={loading}
        style={{ padding: '10px 20px', cursor: 'pointer' }}
      >
        {loading ? "Génération en cours..." : "Générer l'audio"}
      </button>

      {audioUrl && (
        <div style={{ marginTop: '30px' }}>
          <h3>Résultat :</h3>
          <audio src={audioUrl} controls autoPlay />
          <br /><br />
          <a href={audioUrl} download="speech.wav">
            <button style={{ padding: '5px 10px' }}>Télécharger l'audio</button>
          </a>
        </div>
      )}
    </div>
  )
}

export default App