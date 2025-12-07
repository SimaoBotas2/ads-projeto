declare module "swiper/css";
declare module "swiper/css/navigation";

interface AppConfig {
  API_URL: string;
}

interface Window {
  APP_CONFIG: AppConfig;
}
