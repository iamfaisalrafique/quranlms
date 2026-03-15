import { useState, useRef, useEffect } from 'react';

const AudioPlayer = ({ currentAyat, surahNumber, onAyatComplete }) => {
    const audioRef = useRef(null);
    const [reciterId, setReciterId] = useState(7); // Mishary Rashid Alafasy default
    const [isPlaying, setIsPlaying] = useState(false);
    const [progress, setProgress] = useState(0);

    const reciters = [
        { id: 7, name: 'Mishary Rashid Alafasy' },
        { id: 2, name: 'AbdulBaset AbdulSamad' },
        { id: 10, name: 'Saud Ash-Shuraym' }
    ];

    // Format numbers to 3 digits e.g. 1 -> 001
    const padNumber = (num) => num.toString().padStart(3, '0');

    useEffect(() => {
        if (currentAyat && isPlaying) {
            audioRef.current.play().catch(e => console.log('Audio autoplay prevented:', e));
        }
    }, [currentAyat, reciterId]);

    const togglePlay = () => {
        if (isPlaying) {
            audioRef.current.pause();
        } else {
            audioRef.current.play();
        }
        setIsPlaying(!isPlaying);
    };

    const handleTimeUpdate = () => {
        if (audioRef.current) {
            const current = audioRef.current.currentTime;
            const duration = audioRef.current.duration;
            if (duration > 0) {
                setProgress((current / duration) * 100);
            }
        }
    };

    const handleAudioEnded = () => {
        setProgress(0);
        if (onAyatComplete) {
            onAyatComplete();
        }
    };

    if (!currentAyat) return null;

    const audioUrl = `https://verses.quran.com/${reciterId}/${padNumber(surahNumber)}${padNumber(currentAyat)}.mp3`;

    return (
        <div className="fixed-bottom bg-white border-top shadow-sm p-3 d-flex align-items-center justify-content-between" style={{ zIndex: 1000 }}>
            <div className="d-flex align-items-center gap-3">
                <select 
                    className="form-select form-select-sm" 
                    value={reciterId} 
                    onChange={(e) => setReciterId(e.target.value)}
                    style={{ width: '200px' }}
                >
                    {reciters.map(r => (
                        <option key={r.id} value={r.id}>{r.name}</option>
                    ))}
                </select>
                <span className="badge bg-light text-dark border">
                    {surahNumber}:{currentAyat}
                </span>
            </div>

            <div className="d-flex align-items-center gap-4 flex-grow-1 mx-5">
                <button className="btn btn-outline-primary rounded-circle p-2" onClick={() => onAyatComplete(-1)}>
                    <i className="la la-step-backward"></i>
                </button>
                
                <button 
                    className="btn btn-primary rounded-circle d-flex align-items-center justify-content-center" 
                    style={{ width: '50px', height: '50px' }}
                    onClick={togglePlay}
                >
                    <i className={`la ${isPlaying ? 'la-pause' : 'la-play'} fs-3`}></i>
                </button>

                <button className="btn btn-outline-primary rounded-circle p-2" onClick={() => onAyatComplete(1)}>
                    <i className="la la-step-forward"></i>
                </button>

                <div className="progress flex-grow-1" style={{ height: '8px' }}>
                    <div 
                        className="progress-bar bg-primary" 
                        role="progressbar" 
                        style={{ width: `${progress}%` }} 
                        aria-valuenow={progress} 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                    ></div>
                </div>
            </div>

            <audio 
                ref={audioRef}
                src={audioUrl}
                onTimeUpdate={handleTimeUpdate}
                onEnded={handleAudioEnded}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
            />
        </div>
    );
};

export default AudioPlayer;
