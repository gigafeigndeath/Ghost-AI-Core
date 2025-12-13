import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Zap, Clock, Share2, Image, Trophy } from 'lucide-react'

export default function Home() {
  const [url, setUrl] = useState('')

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Hero */}
      <section className="text-center py-20">
        <h1 className="text-5xl md:text-6xl font-bold mb-6">
          Новость живёт всего 3 часа?
        </h1>
        <p className="text-3xl md:text-4xl font-semibold text-indigo-600 mb-8">
          Продли жизнь инфоповодам с помощью ИИ!
        </p>
        <p className="text-xl text-gray-600 max-w-4xl mx-auto mb-12">
          Автоматизируйте PR, сломайте алгоритмы охватов и расширьте продолжительность жизни новостей!
          Ghost AI — цифровое эхо вашего бренда (участие в конкурсе МПИТ).
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <input
            type="url"
            placeholder="Вставьте ссылку на статью..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="px-6 py-4 rounded-lg border border-gray-300 text-lg w-full max-w-md"
          />
          <Link
            to="/dashboard"
            className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition flex items-center justify-center"
          >
            Обработать новость <ArrowRight className="ml-2" />
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-8 my-20">
        <div className="bg-white p-8 rounded-xl shadow-md">
          <Clock className="h-12 w-12 text-indigo-600 mb-4" />
          <h3 className="text-2xl font-bold mb-4">Разный тайминг</h3>
          <p className="text-gray-600">Публикации сразу, через 3 часа и на утро — максимальный охват</p>
        </div>
        <div className="bg-white p-8 rounded-xl shadow-md">
          <Share2 className="h-12 w-12 text-indigo-600 mb-4" />
          <h3 className="text-2xl font-bold mb-4">Адаптация под площадки</h3>
          <p className="text-gray-600">Telegram — коротко, VK — дружелюбно, бизнес-блог — профессионально</p>
        </div>
        <div className="bg-white p-8 rounded-xl shadow-md">
          <Image className="h-12 w-12 text-indigo-600 mb-4" />
          <h3 className="text-2xl font-bold mb-4">Креативные изображения</h3>
          <p className="text-gray-600">Автоматическая генерация иллюстраций через Kandinsky / Stable Diffusion</p>
        </div>
      </section>

      <div className="text-center py-12">
        <Link to="/dashboard" className="inline-flex items-center text-xl font-bold text-indigo-600 hover:text-indigo-800">
          Перейти в личный кабинет <ArrowRight className="ml-2" />
        </Link>
      </div>
    </div>
  )
}