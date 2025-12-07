type Props = {
  show: boolean;
  type: "success" | "error";
  message: string;
  onClose: () => void;
};

export default function AuthModal({ show, type, message, onClose }: Props) {
  if (!show) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex justify-center items-center z-50">
      <div className="bg-[#1E1E1E] p-6 rounded-2xl shadow-xl max-w-sm w-full border border-[#03DAC680] text-center animate-fade-in">
        <h2
          className={
            type === "success"
              ? "text-[#03DAC6] text-xl font-bold mb-3"
              : "text-red-400 text-xl font-bold mb-3"
          }
        >
          {type === "success" ? "Sucesso" : "Erro"}
        </h2>

        <p className="text-[#F5F5F5] mb-6">{message}</p>

        <button
          onClick={onClose}
          className="w-full bg-[#03DAC6] text-black py-2 rounded-full font-semibold 
                     hover:opacity-90 transition duration-300 ease-out cursor-pointer
                     hover:bg-[#019687]"
        >
          OK
        </button>
      </div>
    </div>
  );
}
