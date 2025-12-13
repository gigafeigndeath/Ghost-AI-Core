import { useState } from 'react'
import axios from 'axios'
import { Copy, Check, Zap, Image as ImageIcon, Send, Trophy } from 'lucide-react'

export default function Dashboard() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [posts, setPosts] = useState([])
  const [copiedIndex, setCopiedIndex] = useState(null)
 
const handleAnalyze = async () => {
    if (!articleUrl.trim()) return;

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/generate_posts?url=${encodeURIComponent(articleUrl.trim())}`, {
            method: 'GET',
        });

        if (!response.ok) throw new Error('Ошибка');
        const data = await response.json();
        // обработка data (посты)
    } catch (err) {
        // ошибка
    }
};

const handleAnalyze = async () => {
    if (!articleUrl.trim()) return;

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/generate_posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: articleUrl.trim() })  // точный JSON с "url"
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка обработки');
        }

        const data = await response.json();
        // обработка data (посты, картинки)
    } catch (err) {
        // показ "Ошибка обработки статьи"
    }
};


const handleAnalyze = async () => {
    if (!articleUrl.trim()) return;

    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/generate_posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: articleUrl.trim() })  // точный JSON с "url"
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка обработки');
        }

        const data = await response.json();
        // обработка data (посты, картинки)
    } catch (err) {
        // показ "Ошибка обработки статьи"
    }
}

const handleSubmit = async (articleUrl) => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/generate_posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // ключевой заголовок
            },
            body: JSON.stringify({ url: articleUrl.trim() })  // ключевой фикс — JSON с "url"
        });

        if (!response.ok) throw new Error('Error');
        const data = await response.json();
        // обработка data (посты, картинки)
    } catch (err) {
        // ошибка
    }
};
const handleAnalyze = async () => {
    if (!url) return
    setLoading(true)
    try {
      const res = await axios.post('/api/analyze/generate_posts', {
        url,
        platforms: ['telegram', 'vk', 'business']
      })
      setPosts(res.data.posts)
    } catch (err) {
      alert('Ошибка обработки статьи')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text, index) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(0)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
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
            className="flex-1 px-6 py-4 border rounded-lg text-lg"
            onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-indigo-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-indigo-700 transition flex items-center"
          >
            {loading ? 'Обработка...' : <>Обработать статью <Zap className="ml-2" /></>}
          </button>
        </div>
      </div>

      {posts.length > 0 && (
        <div className="space-y-8">
          <h2 className="text-3xl font-bold text-center">Ваш медиаплан</h2>
          {posts.map((post, i) => (
            <div key={i} className="bg-white rounded-xl shadow-md overflow-hidden">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-4">
                <h3 className="text-xl font-bold">{post.platform.toUpperCase()}</h3>
                <p className="text-sm opacity-90">Публикация: {post.time === 'now' ? 'Сейчас' : post.time}</p>
              </div>
              <div className="p-6">
                <p className="text-lg mb-4 whitespace-pre-wrap">{post.content}</p>
                <div className="flex gap-4">
                  <button
                    onClick={() => copyToClipboard(post.content, i)}
                    className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded hover:bg-gray-200 transition"
                  >
                    {copiedIndex === i ? <Check className="h-5 w-5 text-green-600" /> : <Copy className="h-5 w-5" />}
                    Копировать
                    </button>
                  <button className="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition">
                    <ImageIcon className="h-5 w-5" />
                    Сгенерировать изображение
                  </button>
                  <button className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200 transition">
                    <Send className="h-5 w-5" />
                    Опубликовать
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
