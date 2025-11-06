import { useState } from "react";
import { Eye, EyeOff, Film } from "lucide-react";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="bg-linear-to-b from-[#121212] to-[#1E1E1E] text-[#F5F5F5] min-h-screen flex flex-col justify-center items-center px-6">
      <div className="flex flex-col items-center mb-10">
        <div className="flex items-center space-x-2">
          <Film className="text-[#03DAC6] h-10 w-10" />
          <h1 className="text-3xl font-bold text-[#03DAC6]">CineScope</h1>
        </div>
        <p className="text-[#BBBBBB] mt-2 text-sm">
          {isLogin
            ? "Sign in to your account"
            : "Create your account to start exploring"}
        </p>
      </div>
      <div className="bg-[#1E1E1E] rounded-2xl p-8 shadow-xl w-full max-w-md">
        <form className="space-y-6">
          {!isLogin && (
            <div>
              <label className="block text-sm mb-2">Username</label>
              <input
                type="text"
                placeholder="Enter your username"
                className="w-full bg-[#2A2A2A] rounded-full py-3 px-4 text-[#F5F5F5] placeholder:text-[#BBBBBB] focus:outline-none focus:ring-2 focus:ring-[#03DAC6]"
              />
            </div>
          )}

          <div>
            <label className="block text-sm mb-2">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              className="w-full bg-[#2A2A2A] rounded-full py-3 px-4 text-[#F5F5F5] placeholder:text-[#BBBBBB] focus:outline-none focus:ring-2 focus:ring-[#03DAC6]"
            />
          </div>

          <div>
            <label className="block text-sm mb-2">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                className="w-full bg-[#2A2A2A] rounded-full py-3 px-4 text-[#F5F5F5] placeholder:text-[#BBBBBB] focus:outline-none focus:ring-2 focus:ring-[#03DAC6]"
              />
              {showPassword ? (
                <EyeOff
                  onClick={() => setShowPassword(false)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-[#BBBBBB] cursor-pointer hover:text-[#03DAC6]"
                />
              ) : (
                <Eye
                  onClick={() => setShowPassword(true)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-[#BBBBBB] cursor-pointer transition ease-out hover:text-[#03DAC6]"
                />
              )}
            </div>
          </div>

          <button
            type="submit"
            className="relative w-full cursor-pointer font-bold py-3 rounded-full text-white 
             overflow-hidden transition-all duration-500 ease-out
             bg-[#03DAC6] hover:text-white group shadow-lg shadow-[#03DAC640]"
          >
            <span
              className="absolute inset-0 bg-linear-to-r from-[#BB86FC] via-[#03DAC6] to-[#BB86FC]
                   opacity-0 group-hover:opacity-100 group-hover:animate-gradient-flow"
            ></span>
            <span className="relative z-10">
              {isLogin ? "Sign In" : "Sign Up"}
            </span>
          </button>
        </form>

        <p className="text-center text-[#BBBBBB] mt-6 text-sm">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            className="text-[#03DAC6] cursor-pointer hover:underline font-semibold"
          >
            {isLogin ? "Sign up" : "Sign in"}
          </button>
        </p>
      </div>
    </div>
  );
}
