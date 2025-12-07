import { useContext, useState } from "react";
import { Eye, EyeOff, Film } from "lucide-react";
import { useForm } from "react-hook-form";
import apiRequest from "../lib/apiRequest";
import AuthModal from "../components/modal";
import { AuthContext } from "../context/authContext";

interface AuthFormData {
  username?: string;
  email: string;
  password: string;
}

interface ApiError {
  response?: {
    data?: {
      detail?: string;
    };
  };
}

export default function AuthPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const { register, handleSubmit, reset } = useForm<AuthFormData>();
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState("");
  const [modalType, setModalType] = useState<"success" | "error">("success");
  const { updateUser, updateToken } = useContext(AuthContext);

  const onSubmit = handleSubmit(async (data: AuthFormData) => {
    setIsLoading(true);
    const validations = Validations(
      data,
      isLogin,
      setModalType,
      setModalMessage,
      setShowModal,
      setIsLoading
    );
    if (!validations) {
      console.error("Validation failed");
      return;
    }

    try {
      const endpoint = isLogin ? "login" : "register";

      const response = await apiRequest.post(`/users/${endpoint}`, {
        ...data,
        bio: "This is a sample bio",
      });

      if (isLogin) {
        updateUser(response.data.user);
        updateToken(response.data.access_token);

        setModalType("success");
        setModalMessage("Login realizado com sucesso!");
        setShowModal(true);

        window.location.href = "/home";
      } else {
        setModalType("success");
        setModalMessage("Conta criada com sucesso, faça login para continuar.");
        setShowModal(true);
        setIsLogin(true);
      }

      reset();
    } catch (error) {
      const backendMessage =
        (error as ApiError)?.response?.data?.detail ||
        "Ocorreu um erro durante a autenticação.";

      setModalType("error");
      setModalMessage(backendMessage);
      setShowModal(true);

      console.error("Error during authentication:", error);
    } finally {
      setIsLoading(false);
    }
  });

  return (
    <div className="bg-linear-to-b from-[#121212] to-[#1E1E1E] text-[#F5F5F5] min-h-screen flex flex-col justify-center items-center px-6 relative">
      {showModal && (
        <AuthModal
          show={showModal}
          type={modalType}
          message={modalMessage}
          onClose={() => {
            setShowModal(false);
            if (modalType === "success" && !isLogin) {
              setIsLogin(true);
            }
          }}
        />
      )}

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
        <form className="space-y-6" onSubmit={onSubmit}>
          {!isLogin && (
            <div className="space-y-4">
              <label className="block text-sm mb-2">Username</label>
              <input
                type="text"
                {...register("username")}
                placeholder="Enter your username"
                required
                className="w-full bg-[#2A2A2A] rounded-full py-3 px-4 text-[#F5F5F5] placeholder:text-[#BBBBBB] focus:outline-none focus:ring-2 focus:ring-[#03DAC6]"
              />
              <div>
                <label className="block text-sm mb-2">Email</label>
                <input
                  type="email"
                  {...register("email")}
                  placeholder="you@example.com"
                  required
                  className="w-full bg-[#2A2A2A] rounded-full py-3 px-4 text-[#F5F5F5] placeholder:text-[#BBBBBB] focus:outline-none focus:ring-2 focus:ring-[#03DAC6]"
                />
              </div>
            </div>
          )}

          {isLogin && (
            <div>
              <label className="block text-sm mb-2">Email/Username</label>
              <input
                type="text"
                {...register("username")}
                placeholder="Enter your email or username"
                required
                className="w-full bg-[#2A2A2A] rounded-full py-3 px-4 text-[#F5F5F5] placeholder:text-[#BBBBBB] focus:outline-none focus:ring-2 focus:ring-[#03DAC6]"
              />
            </div>
          )}

          <div>
            <label className="block text-sm mb-2">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                {...register("password")}
                required
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
            disabled={isLoading}
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

function Validations(
  data: AuthFormData,
  isLogin: boolean,
  setModalType: (type: "success" | "error") => void,
  setModalMessage: (message: string) => void,
  setShowModal: (show: boolean) => void,
  setIsLoading: (loading: boolean) => void
) {
  if (isLogin) {
    if (!data.username || !data.password) {
      setModalType("error");
      setModalMessage("Por favor, preencha username e password.");
      setShowModal(true);
      setIsLoading(false);
      return false;
    }
    return true;
  }

  if (!data.username || !data.email || !data.password) {
    setModalType("error");
    setModalMessage("Por favor, preencha todos os campos obrigatórios.");
    setShowModal(true);
    setIsLoading(false);
    return false;
  }

  const isEmailValid = validateEmail(data.email);
  if (!isEmailValid) {
    setModalType("error");
    setModalMessage("Por favor, insira um endereço de email válido.");
    setShowModal(true);
    setIsLoading(false);
    return false;
  }

  const isPasswordValid = validatePassword(data.password);
  if (!isPasswordValid) {
    setModalType("error");
    setModalMessage(
      "A senha deve ter pelo menos 8 caracteres, incluindo um número e um caractere especial."
    );
    setShowModal(true);
    setIsLoading(false);
    return false;
  }

  return true;
}

function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validatePassword(password: string): boolean {
  const passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{8,}$/;
  return passwordRegex.test(password);
}
