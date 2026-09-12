import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from '../locales/en.json'
import hi from '../locales/hi.json'
import mr from '../locales/mr.json'

const savedLang = localStorage.getItem('asa_language') || 'en'

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    hi: { translation: hi },
    mr: { translation: mr },
  },
  lng: savedLang,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
})

export function changeLanguage(lang) {
  i18n.changeLanguage(lang)
  localStorage.setItem('asa_language', lang)
}

export default i18n
