// frontend/page.js
export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-96 border border-gray-700">
        <h1 className="text-2xl font-bold text-white mb-6 text-center">
          ARM TechBridge AI
        </h1>
        <form className="space-y-4">
          <div>
            <label className="text-gray-400 text-sm">Email Workspace ID</label>
            <input 
              type="email" 
              defaultValue="armtechbridge@gmail.com"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </div>
          <div>
            <label className="text-gray-400 text-sm">Password</label>
            <input 
              type="password" 
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </div>
          <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition duration-200">
            Secure Login
          </button>
        </form>
      </div>
    </div>
  );
}
