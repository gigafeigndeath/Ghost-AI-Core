import { useState } from 'react'  
import { Copy, Check, Zap, Image as ImageIcon, Send, Trophy, Loader2 } from 'lucide-react'  

export default function Dashboard() {  
  const [url, setUrl] = useState('')  
  const [loading, setLoading] = useState(false)  
  const [error, setError] = useState('')  
  const [mediaPlan, setMediaPlan] = useState(null)  
  const [copiedIndex, setCopiedIndex] = useState(null)  

  const handleAnalyze = async () => {  
    if (!url.trim()) {  
      setError('Введите URL статьи')  
      return  
    }  
    setLoading(true)  
    setError('')  
    setMediaPlan(null)  
    try {  
      const res = await fetch('/api/analyze/generate_posts', {  
        method: 'POST',  
        headers: { 'Content-Type': 'application/json' },  
        body: JSON.stringify({ url: url.trim() })  
      })  
      if (!res.ok) {  
        const errData = await res.json()  
        throw new Error(errData.detail || 'Ошибка обработки статьи')  
      }  
      const data = await res.json()
      if (data.error) {  
        setError(data.error);  
        setMediaPlan(null);  
      } else {  
        setMediaPlan(data);  
      }    
      setMediaPlan(data)  
    } catch (err) {  
      setError(err.message || 'Ошибка обработки статьи')  
    } finally {  
      setLoading(false)  
    }  
  }  

  const copyToClipboard = (text, index) => {  
    navigator.clipboard.writeText(text)  
    setCopiedIndex(index)  
    setTimeout(() => setCopiedIndex(null), 2000)  
  }  

  const regenerateImage = async (platform) => {  
    // Логика регенерации (POST /api/regenerate_image) — добавьте эндпоинт в api.py  
    console.log(`Регенерация изображения для ${platform}`)  
  }  

  const publishPost = async (platform, content, image) => {  
    try {  
      const res = await fetch('/api/publish', {  
        method: 'POST',  
        headers: { 'Content-Type': 'application/json' },  
        body: JSON.stringify({ post_type: platform, content, image_url: image })  
      })  
      if (!res.ok) throw new Error('Ошибка публикации')  
      alert('Опубликовано!')  
    } catch (err) {  
      alert(err.message)  
    }  
  }  

  const platforms = mediaPlan ? [  
    { key: 'telegram', title: 'Telegram', time: mediaPlan.timings.telegram, gradient: 'from-cyan-500 to-blue-600' },  
    { key: 'vk', title: 'ВКонтакте', time: mediaPlan.timings.vk, gradient: 'from-blue-500 to-indigo-600' },  
    { key: 'blog', title: 'Бизнес-блог (VC)', time: mediaPlan.timings.blog, gradient: 'from-purple-500 to-pink-600' }  
  ] : []  

  return (  
    <div className="max-w-5xl mx-auto px-4 py-12">  
      <div className="text-center mb-12">  
        <h1 className="text-4xl font-bold mb-4">Личный кабинет Ghost AI</h1>  
        <p className="text-lg text-gray-600 flex items-center justify-center">  
          <Trophy className="h-6 w-6 mr-2 text-yellow-500" />  
          Участие в конкурсе МПИТ — автономный PR-агент нового поколения  
        </p>  
      </div>  
      <div className="bg-white rounded-xl shadow-lg p-8 mb-12">  
        <div className="flex gap-4">  
          <input  
            type="url"  
            placeholder="https://example.com/news-about-your-company"  
            value={url}  
            onChange={(e) => setUrl(e.target.value)}  
            onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}  
            className="flex-1 px-6 py-4 border rounded-lg text-lg"  
            disabled={loading}  
          />  
          <button  
            onClick={handleAnalyze}  
            disabled={loading}  
            className="bg-indigo-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-indigo-700 transition flex items-center"  
          >  
            {loading ? (  
              <>  
                <Loader2 className="animate-spin mr-2 h-5 w-5" />  
                Обработка...  
              </>  
            ) : (  
              <>  
                Обработать статью <Zap className="ml-2 h-5 w-5" />  
              </>  
            )}  
          </button>  
        </div>  
        {error && <p className="text-red-500 mt-4 text-center">{error}</p>}  
      </div>  
      {mediaPlan && (  
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">  
          <h2 className="col-span-full text-3xl font-bold text-center mb-6">Ваш медиаплан</h2>  
          {platforms.map((plat, i) => (  
            <div key={plat.key} className="bg-white rounded-xl shadow-md overflow-hidden">  
              <div className={`bg-gradient-to-r ${plat.gradient} text-white p-6`}>  
                <h3 className="text-xl font-bold">{plat.title}</h3>  
                <p className="text-sm opacity-90">Публикация: {plat.time === 'now' ? 'Сейчас' : plat.time === 'in 3-4 hours' ? 'Через 3-4 часа' : 'Завтра утром'}</p>  
              </div>  
              <div className="p-6">  
                <p className="text-lg mb-4 whitespace-pre-wrap">{mediaPlan.posts[plat.key]}</p>  
                <img src={mediaPlan.images[plat.key]} alt={plat.title} className="w-full rounded-lg shadow-md mb-4" />  
                <div className="flex gap-4">  
                  <button  
                    onClick={() => copyToClipboard(mediaPlan.posts[plat.key], i)}  
                    className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded hover:bg-gray-200 transition"  
                  >  
                    {copiedIndex === i ? <Check className="h-5 w-5 text-green-600" /> : <Copy className="h-5 w-5" />}  
                    {copiedIndex === i ? 'Скопировано!' : 'Копировать'}  
                  </button>  
                  <button  
                    onClick={() => regenerateImage(plat.key)}  
                    className="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition"  
                  >  
                    <ImageIcon className="h-5 w-5" />  
                    Сгенерировать изображение  
                  </button>  
                  <button  
                    onClick={() => publishPost(plat.key, mediaPlan.posts[plat.key], mediaPlan.images[plat.key])}  
                    className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200 transition"  
                  >  
                    <Send className="h-5 w-5" />  
                    Опубликовать  
                  </button>  
                </div>  
              </div>  
            </div>  
          ))}  
        </div>  
      )}  
      <footer className="mt-12 text-center text-gray-500">  
        Разработано для конкурса МПИТ. Логотип: [вставьте логотип МПИТ]  
      </footer>  
    </div>  
  )  
}  
