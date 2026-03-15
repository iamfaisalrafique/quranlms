import { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../utils/api';
import toast from 'react-hot-toast';
import JuzNavigator from '../../components/quran/JuzNavigator';
import AudioPlayer from '../../components/quran/AudioPlayer';

const QuranViewer = () => {
    const { surahId } = useParams();
    const [ayats, setAyats] = useState([]);
    const [surahInfo, setSurahInfo] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [activeJuz, setActiveJuz] = useState(1);
    const [playingAyatNumber, setPlayingAyatNumber] = useState(null);
    const [expandedTafsir, setExpandedTafsir] = useState(null);

    const ayatRefs = useRef({});

    useEffect(() => {
        fetchAyats();
    }, [surahId]);

    const fetchAyats = async () => {
        setIsLoading(true);
        try {
            // First fetch surah info
            const surahRes = await api.get(`/quran/surahs/${surahId}/`);
            setSurahInfo(surahRes.data);

            // Fetch ayats for this surah
            const ayatsRes = await api.get(`/quran/surahs/${surahId}/ayats/`);
            setAyats(ayatsRes.data);
            
            if (ayatsRes.data.length > 0) {
                setActiveJuz(ayatsRes.data[0].juz.number);
            }
        } catch (error) {
            toast.error('Failed to load Quran text');
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleJuzSelect = (juzNumber) => {
        setActiveJuz(juzNumber);
        // Find first ayat in this juz within current surah
        const targetAyat = ayats.find(a => a.juz.number === juzNumber);
        if (targetAyat && ayatRefs.current[targetAyat.number]) {
            ayatRefs.current[targetAyat.number].scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            // If juz is not in this surah, user might want to navigate to it (out of scope for basic viewer, but can be added)
            toast('This Juz is outside the current Surah', { icon: 'ℹ️' });
        }
    };

    const handleAyatComplete = (direction = 1) => {
        if (!playingAyatNumber) return;
        
        const currentIndex = ayats.findIndex(a => a.number === playingAyatNumber);
        if (currentIndex === -1) return;

        const nextIndex = currentIndex + direction;
        if (nextIndex >= 0 && nextIndex < ayats.length) {
            setPlayingAyatNumber(ayats[nextIndex].number);
            ayatRefs.current[ayats[nextIndex].number]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            setPlayingAyatNumber(null); // End of surah
        }
    };

    const toggleBookmark = async (ayatNumber) => {
        try {
            await api.post(`/quran/bookmarks/`, {
                surah: surahId,
                ayat_number: ayatNumber
            });
            toast.success('Bookmark saved!');
        } catch (error) {
            toast.error('Failed to save bookmark');
        }
    };

    if (isLoading) {
        return (
            <div className="d-flex justify-content-center align-items-center vh-100">
                <div className="spinner-border text-primary" role="status"></div>
            </div>
        );
    }

    return (
        <div className="container-fluid pb-5 mb-5 pt-4">
            <Link to="/quran" className="btn btn-outline-primary mb-4">
                <i className="la la-arrow-left me-2"></i> Back to Surahs
            </Link>

            <JuzNavigator currentJuz={activeJuz} onJuzSelect={handleJuzSelect} />

            <div className="card mb-4 border-0 bg-primary text-white text-center py-4 rounded-4" style={{ backgroundImage: "url('/dashboard/assets/images/islamic-pattern.png')", backgroundBlendMode: 'overlay', backgroundSize: 'cover' }}>
                <div className="card-body">
                    <h1 className="display-4 text-white" style={{ fontFamily: "'KFGQPC Uthmanic Script HAFS', serif" }}>
                        {surahInfo?.name_arabic}
                    </h1>
                    <h3 className="mb-0">{surahInfo?.name_english}</h3>
                    <p className="mt-2 mb-0 opacity-75">{surahInfo?.revelation_type} • {surahInfo?.total_ayats} Ayahs</p>
                </div>
            </div>

            {/* Bismillah before Surah (except At-Tawbah) */}
            {surahId !== '9' && (
                <div className="text-center mb-5">
                    <h2 className="text-primary" style={{ fontFamily: "'KFGQPC Uthmanic Script HAFS', serif" }}>
                        بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
                    </h2>
                </div>
            )}

            <div className="quran-reader">
                {ayats.map((ayat) => (
                    <div 
                        key={ayat.id} 
                        ref={el => ayatRefs.current[ayat.number] = el}
                        className={`card mb-3 transition-all ${playingAyatNumber === ayat.number ? 'bg-light border-primary' : ''}`}
                    >
                        <div className="card-header bg-transparent d-flex justify-content-between align-items-center border-0 pt-4 px-4 pb-0">
                            <div className="d-flex gap-2">
                                <span className="badge rounded-pill bg-light text-dark border p-2 px-3 fw-bold shadow-sm d-flex align-items-center gap-2">
                                    <span style={{ color: '#D4AF37' }}>{surahId}</span> : {ayat.number}
                                </span>
                                <button className="btn btn-sm btn-outline-warning rounded-circle" onClick={() => toggleBookmark(ayat.number)} title="Bookmark">
                                    <i className="la la-bookmark"></i>
                                </button>
                                <button 
                                    className={`btn btn-sm rounded-circle ${playingAyatNumber === ayat.number ? 'btn-primary' : 'btn-outline-primary'}`} 
                                    onClick={() => setPlayingAyatNumber(playingAyatNumber === ayat.number ? null : ayat.number)}
                                    title="Play Audio"
                                >
                                    <i className={`la ${playingAyatNumber === ayat.number ? 'la-pause' : 'la-play'}`}></i>
                                </button>
                            </div>
                            <div>
                                <span className="badge bg-light text-dark border">Juz {ayat.juz.number}</span>
                            </div>
                        </div>
                        
                        <div className="card-body px-4 pb-4">
                            {/* Arabic Verse */}
                            <div className="text-end mb-4" dir="rtl">
                                <p 
                                    className="mb-0 lh-lg" 
                                    style={{ 
                                        fontFamily: "'KFGQPC Uthmanic Script HAFS', serif", 
                                        fontSize: '2.2rem',
                                        lineHeight: '2.8 !important',
                                    }}
                                >
                                    {/* Handle word by word if data is structured, else fallback to full text */}
                                    {ayat.words && ayat.words.length > 0 ? (
                                        ayat.words.map((word, wIdx) => (
                                            <span 
                                                key={wIdx} 
                                                className="word-hover mx-1 d-inline-block text-center" 
                                                title={word.translation_en || word.transliteration}
                                                style={{ cursor: 'pointer', transition: 'color 0.2s' }}
                                                onMouseEnter={(e) => e.target.style.color = '#1A6B4A'}
                                                onMouseLeave={(e) => e.target.style.color = 'inherit'}
                                            >
                                                {word.text_uthmani}
                                            </span>
                                        ))
                                    ) : (
                                        ayat.text_uthmani
                                    )}
                                    <span className="ms-2 verse-end d-inline-flex align-items-center justify-content-center" style={{ 
                                        width: '40px', height: '40px', 
                                        backgroundImage: "url('/dashboard/assets/images/ayah-end.svg')", 
                                        backgroundSize: 'contain', backgroundRepeat: 'no-repeat', backgroundPosition: 'center',
                                        fontSize: '1rem', color: '#1A6B4A'
                                    }}>
                                        {/* Convert to arabic numerals if desired, fallback to standard */}
                                        {ayat.number}
                                    </span>
                                </p>
                            </div>

                            {/* Translations */}
                            <div className="translations border-start border-4 border-primary ps-3 mt-4">
                                <div className="mb-3">
                                    <h6 className="text-muted mb-1 fs-12 text-uppercase">English (Sahih International)</h6>
                                    <p className="mb-0 fs-16 text-dark">{ayat.translation_en}</p>
                                </div>
                                <div>
                                    <h6 className="text-muted mb-1 fs-12 text-uppercase">Urdu (Jalandhari)</h6>
                                    <p className="mb-0 fs-18 text-dark" dir="rtl" style={{ fontFamily: "'Amiri', serif" }}>{ayat.translation_ur}</p>
                                </div>
                            </div>
                            
                            {/* Tafsir Toggle */}
                            <div className="mt-3 text-end">
                                <button 
                                    className="btn btn-sm btn-link text-decoration-none" 
                                    onClick={() => setExpandedTafsir(expandedTafsir === ayat.number ? null : ayat.number)}
                                >
                                    {expandedTafsir === ayat.number ? 'Hide Tafsir' : 'Read Tafsir (Ibn Kathir)'} <i className={`la ${expandedTafsir === ayat.number ? 'la-angle-up' : 'la-angle-down'}`}></i>
                                </button>
                            </div>

                            {expandedTafsir === ayat.number && (
                                <div className="mt-3 p-3 bg-light rounded shadow-sm border">
                                    <h6 className="text-primary border-bottom pb-2">Tafsir Ibn Kathir</h6>
                                    <div className="tafsir-content" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                                        {ayat.tafsirs && ayat.tafsirs.length > 0 
                                            ? <p className="mb-0 fs-14" dangerouslySetInnerHTML={{ __html: ayat.tafsirs[0].text }}></p>
                                            : <p className="text-muted mb-0 fs-14">Tafsir not available for this ayah.</p>
                                        }
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {playingAyatNumber && (
                <AudioPlayer 
                    currentAyat={playingAyatNumber} 
                    surahNumber={parseInt(surahId)} 
                    onAyatComplete={handleAyatComplete} 
                />
            )}
        </div>
    );
};

export default QuranViewer;
