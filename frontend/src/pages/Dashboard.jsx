import { useState, useEffect } from 'react'
import { Copy, Check, Zap, Image as ImageIcon, Send, Trophy, Loader2 } from 'lucide-react'

export default function Dashboard() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [mediaPlan, setMediaPlan] = useState(null)
  const [copiedIndex, setCopiedIndex] = useState(null)
  const [imageLoading, setImageLoading] = useState({})

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const urlFromQuery = params.get('url')
    if (urlFromQuery) {
      const decoded = decodeURIComponent(urlFromQuery)
      if (decoded.trim()) {
        setUrl(decoded)
        handleAnalyze(decoded)
        window.history.replaceState({}, document.title, '/dashboard')
      }
    }
  }, [])

  const handleAnalyze = async (inputUrl = url) => {
    const currentUrl = typeof inputUrl === 'string' ? inputUrl : url
    if (!currentUrl?.trim()) {
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
        body: JSON.stringify({ url: currentUrl.trim() })
      })
      if (!res.ok) throw new Error((await res.json()).detail || 'Ошибка сервера')
      const data = await res.json()
      setMediaPlan(data)
    } catch (err) {
      setError(err.message || 'Ошибка обработки статьи')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text, index) => {
    const fallback = () => {
      const el = document.createElement('textarea')
      el.value = text
      document.body.appendChild(el)
      el.select()
      document.execCommand('copy')
      document.body.removeChild(el)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    }
    navigator.clipboard?.writeText(text)?.then(() => {
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    }) ?? fallback()
  }

  const regenerateImage = async (platform, index) => {
    setImageLoading(p => ({ ...p, [index]: true }))
    try {
      const res = await fetch('/api/regenerate_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ platform, prompt: mediaPlan.posts[platform] })
      })
      const data = await res.json()
      setMediaPlan(p => ({
        ...p,
        images: { ...p.images, [platform]: data.image_url || null }
      }))
    } catch {
      alert('Ошибка генерации изображения')
    } finally {
      setImageLoading(p => ({ ...p, [index]: false }))
    }
  }

  // Автопостинг только в Telegram (один клик!)
  const publishPost = async (platform, content, image) => {
    if (platform !== 'telegram') {
      alert('Автопостинг сейчас доступен только в Telegram')
      return
    }

    try {
      const res = await fetch('/api/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post_type: 'telegram', content, image_url: image || null })
      })

      if (!res.ok) {
        const errText = await res.text()
        throw new Error(errText || 'Ошибка публикации')
      }

      alert('✅ Пост успешно опубликован в вашем Telegram-канале!\n\nНовость получила вторую жизнь благодаря Ghost AI 🚀')
    } catch (err) {
      console.error(err)
      alert('Ошибка автопостинга: ' + err.message)
    }
  }

  const platforms = mediaPlan ? [
    { key: 'telegram', title: 'Telegram', time: mediaPlan.timings.telegram, gradient: 'from-cyan-500 to-blue-600' },
    { key: 'vk', title: 'ВКонтакте', time: mediaPlan.timings.vk, gradient: 'from-blue-500 to-indigo-600' },
    { key: 'blog', title: 'Бизнес-блог (VC)', time: mediaPlan.timings.blog, gradient: 'from-purple-500 to-pink-600' }
  ] : []

  const ghostPlaceholder = "https://static.vecteezy.com/system/resources/thumbnails/048/332/703/small/cartoon-cute-ghost-character-isolated-on-the-transparent-background-png.png"

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">Личный кабинет Ghost AI</h1>
        <p className="text-lg sm:text-xl text-gray-600 flex items-center justify-center">
          <Trophy className="h-6 w-6 mr-2 text-yellow-500" />
          Участие в конкурсе МПИТ — автономный PR-агент нового поколения
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 sm:p-8 mb-12">
        <div className="flex flex-col lg:flex-row gap-4">
          <input
            type="url"
            placeholder="https://example.com/news-about-your-company"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
            className="flex-1 px-6 py-4 border rounded-lg text-lg w-full"
            disabled={loading}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-indigo-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-indigo-700 transition flex items-center justify-center"
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
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
          <h2 className="col-span-full text-3xl sm:text-4xl font-bold text-center mb-8">
            Ваш медиаплан
          </h2>

          {platforms.map((plat, i) => (
            <div key={plat.key} className="bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
              <div className={`bg-gradient-to-r ${plat.gradient} text-white p-6 sm:p-8`}>
                <h3 className="text-xl sm:text-2xl font-bold">{plat.title}</h3>
                <p className="text-sm sm:text-base opacity-90">
                  Публикация: {plat.time === 'now' ? 'Сейчас' : plat.time === 'in 3-4 hours' ? 'Через 3-4 часа' : 'Завтра утром'}
                </p>
              </div>

              <div className="p-6 sm:p-8 flex-grow flex flex-col">
                <p className="text-base sm:text-lg mb-6 whitespace-pre-wrap flex-grow">
                  {mediaPlan.posts[plat.key]}
                </p>

                {mediaPlan.images[plat.key] ? (
                  <img
                    src={mediaPlan.images[plat.key]}
                    alt={plat.title}
                    className="w-full rounded-lg shadow-md mb-6 object-cover h-64"
                  />
                ) : (
                  <div className="w-full h-64 rounded-lg shadow-md mb-6 overflow-hidden bg-gray-50 flex items-center justify-center">
                    <img src={ghostPlaceholder} alt="Призрак" className="max-w-full max-h-full object-contain" />
                  </div>
                )}

                <div className="flex flex-col gap-4 mt-auto">
                  <button
                    onClick={() => copyToClipboard(mediaPlan.posts[plat.key], i)}
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-gray-100 rounded hover:bg-gray-200 transition font-medium"
                  >
                    {copiedIndex === i ? <Check className="h-5 w-5 text-green-600" /> : <Copy className="h-5 w-5" />}
                    {copiedIndex === i ? 'Скопировано!' : 'Копировать текст'}
                  </button>

                  <button
                    onClick={() => regenerateImage(plat.key, i)}
                    disabled={imageLoading[i]}
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition font-medium"
                  >
                    {imageLoading[i] ? <Loader2 className="animate-spin h-5 w-5" /> : <ImageIcon className="h-5 w-5" />}
                    {imageLoading[i] ? 'Генерация...' : 'Новая картинка'}
                  </button>

                  {/* Автопостинг только для Telegram */}
                  {plat.key === 'telegram' && (
                    <button
                      onClick={() => publishPost(plat.key, mediaPlan.posts[plat.key], mediaPlan.images[plat.key])}
                      className="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg hover:shadow-xl transform hover:scale-105 transition font-bold text-lg shadow-lg"
                    >
                      <Send className="h-6 w-6" />
                      Автопостинг в канал — 1 клик!
                    </button>
                  )}

                  {/* Для VK и блога — просто копирование */}
                  {plat.key !== 'telegram' && (
                    <button
                      onClick={() => copyToClipboard(mediaPlan.posts[plat.key], i)}
                      className="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-gray-400 to-gray-600 text-white rounded-lg font-bold text-lg"
                    >
                      <Copy className="h-6 w-6" />
                      Копировать для {plat.title}
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <footer className="mt-16 text-center text-gray-500">
        Разработано для конкурса МПИТ 2025 • Автономный PR-агент нового поколения
      </footer>
    </div>
  )
}
