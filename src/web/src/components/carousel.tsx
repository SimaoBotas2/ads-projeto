import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation } from "swiper/modules";
import { ChevronLeft, ChevronRight } from "lucide-react";
import "swiper/css";
import "swiper/css/navigation";
import { useRef } from "react";
import type { Swiper as SwiperClass } from "swiper";

interface CarouselProps {
  title: string;
  items: { title: string; rating?: string }[];
}

export default function RecommendationsCarousel({
  title,
  items,
}: CarouselProps) {
  const swiperRef = useRef<SwiperClass | null>(null);

  return (
    <section className="p-6 relative transition-opacity duration-500 ease-in-out">
      <h2 className="text-xl font-bold mb-4 text-[#F5F5F5]">{title}</h2>

      <button
        onClick={() => swiperRef.current?.slidePrev()}
        className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-[#1E1E1E] cursor-pointer hover:bg-[#bb86fc8c] p-2 rounded-full shadow-md transition-colors"
      >
        <ChevronLeft className="text-[#03DAC6] h-6 w-6" />
      </button>

      <button
        onClick={() => swiperRef.current?.slideNext()}
        className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-[#1E1E1E] cursor-pointer hover:bg-[#bb86fc8c] p-2 rounded-full shadow-md transition-colors"
      >
        <ChevronRight className="text-[#03DAC6] h-6 w-6" />
      </button>

      <Swiper
        modules={[Navigation]}
        spaceBetween={16}
        slidesPerView={4}
        onSwiper={(swiper) => (swiperRef.current = swiper)}
        className="pb-6"
        breakpoints={{
          640: { slidesPerView: 2 },
          768: { slidesPerView: 3 },
          1024: { slidesPerView: 4 },
        }}
      >
        {items.map((item, idx) => (
          <SwiperSlide
            key={idx}
            className="hover:cursor-pointer active:cursor-grabbing"
          >
            <div className="bg-[#1E1E1E] rounded-lg overflow-hidden hover:shadow-xl transition">
              <div className="h-64 bg-gray-700"></div>
              <div className="p-2">
                <h3 className="font-bold text-sm text-[#F5F5F5]">
                  {item.title}
                </h3>
                <p className="text-[#BBBBBB] text-xs mt-1">
                  Rating: {item.rating || "⭐⭐⭐☆"}
                </p>
              </div>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
}
