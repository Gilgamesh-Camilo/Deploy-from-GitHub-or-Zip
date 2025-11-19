        import { useState } from 'react'

        export default function App(){
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [fileId, setFileId] = useState(null)

  async function upload(){
    if(!file) return
    const fd = new FormData()
    fd.append('file', file)
    try{
      const res = await fetch(import.meta.env.VITE_API_URL + '/upload-csv', { method: 'POST', body: fd })
      const j = await res.json()
      setPreview(j.preview)
      setFileId(j.id)
    }catch(e){
      alert('Upload failed: ' + e.message)
    }
  }

  return (
    <div style={{padding:20, maxWidth:900, margin:'0 auto'}}>
      <h1>CSV ML Playground</h1>
      <p>Sube un CSV y pruébalo con modelos simples.</p>
      <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} />
      <button onClick={upload} style={{marginLeft:10}}>Subir CSV</button>
      {fileId && <div style={{marginTop:10}}>File ID: <strong>{fileId}</strong></div>}
      {preview && <pre style={{background:'#f7f7f7', padding:10}}>{JSON.stringify(preview, null, 2)}</pre>}
    </div>
  )
}
