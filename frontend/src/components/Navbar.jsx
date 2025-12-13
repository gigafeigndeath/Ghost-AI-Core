import { Link } from 'react-router-dom'
import { Zap, Trophy } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="flex items-center space-x-3">
            <Zap className="h-8 w-8 text-indigo-600" />
            <span className="text-2xl font-bold text-gray-900">Ghost AI</span>
          </Link>
          <div className="flex items-center space-x-6">
            <span className="text-sm text-gray-600 flex items-center">
              <Trophy className="h-5 w-5 mr-2 text-yellow-500" />
              Участие в конкурсе МПИТ
            </span>
            <Link to="/dashboard" className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition">
              Личный кабинет
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}