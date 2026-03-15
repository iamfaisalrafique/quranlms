const JuzNavigator = ({ currentJuz, onJuzSelect }) => {
    // Generate array 1..30
    const juzList = Array.from({ length: 30 }, (_, i) => i + 1);

    return (
        <div className="card mb-4">
            <div className="card-body p-3">
                <div className="d-flex overflow-auto gap-2 py-2" style={{ scrollbarWidth: 'thin' }}>
                    {juzList.map(juz => (
                        <button
                            key={juz}
                            className={`btn btn-sm text-nowrap flex-shrink-0 ${currentJuz === juz ? 'btn-primary' : 'btn-outline-light text-dark border'}`}
                            onClick={() => onJuzSelect(juz)}
                        >
                            Juz {juz}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default JuzNavigator;
