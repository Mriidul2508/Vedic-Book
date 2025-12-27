from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///priest_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class Priest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='priest', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    ceremony_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    time_slot = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    priest_id = db.Column(db.Integer, db.ForeignKey('priest.id'), nullable=True)

# --- Detailed Data (Matching your file extensions exactly) ---
SANSKARS = [
    {
        "id": 1, "name": "Garbhadhana", "name_hi": "गर्भाधान", "purpose": "Conception", "age": "Pre-birth",
        "image": "garbhadhana.png", # PNG
        "mantra": "ॐ अहीनां त्वा पत्नीममिष्यामि कंसां त्वा पत्नीममिष्यामि ।",
        "desc_en": "The act of conception. Parents pray for a healthy and noble child.",
        "desc_hi": "यह पहला संस्कार है। माता-पिता एक स्वस्थ और गुणवान संतान के लिए प्रार्थना करते हैं।"
    },
    {
        "id": 2, "name": "Pumsavana", "name_hi": "पुंसवन", "purpose": "Fetus protection", "age": "3rd month",
        "image": "pumsavana.png", # PNG
        "mantra": "ॐ पुमांसं पुत्रं जनय तं पुमाननु जायताम् ।",
        "desc_en": "Performed to ensure the health of the fetus and mother.",
        "desc_hi": "यह संस्कार गर्भस्थ शिशु और माता के स्वास्थ्य की रक्षा के लिए किया जाता है।"
    },
    {
        "id": 3, "name": "Simantonnayana", "name_hi": "सीमन्तोन्नयन", "purpose": "Mental growth", "age": "7th month",
        "image": "simantonnayana.jpg",
        "mantra": "ॐ येनादितेः सीमानं नयति प्रजापतिर्महते सौभगाय ।",
        "desc_en": "'Baby Shower'. Performed to cheer expecting mother.",
        "desc_hi": "इसे 'गोद भराई' भी कहा जाता है। इसका उद्देश्य गर्भवती माँ को प्रसन्न रखना है।"
    },
    {
        "id": 4, "name": "Jatakarma", "name_hi": "जातकर्म", "purpose": "Newborn welcoming", "age": "At birth",
        "image": "jatakarma.jpg",
        "mantra": "ॐ अंगादंगात्संभवसि हृदयादधिजायसे ।",
        "desc_en": "Performed immediately after birth. The father welcomes the soul.",
        "desc_hi": "जन्म के तुरंत बाद पिता बच्चे को शहद और घी चटाकर स्वागत करते हैं।"
    },
    {
        "id": 5, "name": "Namakarana", "name_hi": "नामकरण", "purpose": "Naming ceremony", "age": "11th day",
        "image": "namakarana.jpg",
        "mantra": "ॐ नाम्ना हि त्वा देवानां नामधेयेन दधामि ।",
        "desc_en": "The child is given a formal name based on astrological calculations.",
        "desc_hi": "ज्योतिषीय गणना के आधार पर बच्चे को एक औपचारिक नाम दिया जाता है।"
    },
    {
        "id": 6, "name": "Nishkramana", "name_hi": "निष्क्रमण", "purpose": "First outing", "age": "4th month",
        "image": "nishkramana.jpg",
        "mantra": "ॐ निष्क्रामतादायुषे वर्चसे प्रजायै रायस्पोषाय ।",
        "desc_en": "The child is taken out for the first time to see the sun and nature.",
        "desc_hi": "बच्चे को पहली बार घर से बाहर सूर्य और प्रकृति के दर्शन के लिए निकाला जाता है।"
    },
    {
        "id": 7, "name": "Annaprashana", "name_hi": "अन्नप्राशन", "purpose": "First solid food", "age": "6th month",
        "image": "annaprashana.jpg",
        "mantra": "ॐ अन्नपतेऽन्नस्य नो धेह्यनमीवस्य शुष्मिणः ।",
        "desc_en": "The first feeding of solid food (usually rice kheer).",
        "desc_hi": "बच्चे को पहली बार ठोस आहार (खीर) खिलाया जाता है।"
    },
    {
        "id": 8, "name": "Chudakarana", "name_hi": "चूड़ाकर्म", "purpose": "First haircut", "age": "1-3 years",
        "image": "chudakarana.jpg",
        "mantra": "ॐ येनावपत्सविता क्षुरेण सोमस्य राज्ञो वरुणस्य विद्वान् ।",
        "desc_en": "Shaving of the baby's first hair (Mundan), symbolizing purity.",
        "desc_hi": "बच्चे के जन्म के बाल उतारे जाते हैं (मुंडन), जो स्वच्छता का प्रतीक है।"
    },
    {
        "id": 9, "name": "Karnavedha", "name_hi": "कर्णवेध", "purpose": "Ear piercing", "age": "3-5 years",
        "image": "karnavedha.jpg",
        "mantra": "ॐ भद्रं कर्णेभिः शृणुयाम देवा ।",
        "desc_en": "Piercing of the ears to open inner ears for sacred knowledge.",
        "desc_hi": "कान छिदवाने की रस्म। माना जाता है कि इससे पवित्र ज्ञान सुनने की क्षमता बढ़ती है।"
    },
    {
        "id": 10, "name": "Vidyarambha", "name_hi": "विद्यारम्भ", "purpose": "Intro to alphabet", "age": "5 years",
        "image": "vidyarambha.jpg",
        "mantra": "ॐ सरस्वती नमस्तुभ्यं वरदे कामरूपिणि ।",
        "desc_en": "The child writes their first letter, marking the beginning of education.",
        "desc_hi": "बच्चा अपना पहला अक्षर लिखता है। यह शिक्षा की औपचारिक शुरुआत है।"
    },
    {
        "id": 11, "name": "Upanayana", "name_hi": "उपनयन", "purpose": "Sacred thread", "age": "8-12 years",
        "image": "upanayana.jpg",
        "mantra": "ॐ यज्ञोपवीतं परमं पवित्रं प्रजापतेर्यत्सहजं पुरस्तात् ।",
        "desc_en": "The sacred thread ceremony (Janeu). Initiation into spiritual knowledge.",
        "desc_hi": "जनेऊ संस्कार। बच्चे को आध्यात्मिक ज्ञान में दीक्षित किया जाता है।"
    },
    {
        "id": 12, "name": "Vedarambha", "name_hi": "वेदारम्भ", "purpose": "Study of Vedas", "age": "After Upanayana",
        "image": "vedarambha.jpg",
        "mantra": "ॐ वेदोऽसि येन त्वं देवेभ्यो वेदो भवस्तेन मह्यं वेदो भूयाः ।",
        "desc_en": "The beginning of the formal study of Vedas.",
        "desc_hi": "वेदों और प्राचीन शास्त्रों के अध्ययन का शुभारंभ।"
    },
    {
        "id": 13, "name": "Keshanta", "name_hi": "केशान्त", "purpose": "First beard shave", "age": "16 years",
        "image": "keshanta.jpg",
        "mantra": "ॐ आयुर्दा देवजरसं गृणानो ।",
        "desc_en": "The first shaving of the beard for boys.",
        "desc_hi": "लड़कों के लिए दाढ़ी बनाने की पहली रस्म।"
    },
    {
        "id": 14, "name": "Samavartana", "name_hi": "समावर्तन", "purpose": "Convocation", "age": "~25 years",
        "image": "samavartana.jpg",
        "mantra": "ॐ एष ते कुलधर्मोऽयं एष ते स्वधर्मायं ।",
        "desc_en": "End of student life. Returning home to start householder life.",
        "desc_hi": "विद्यार्थी जीवन की समाप्ति और गृहस्थ जीवन शुरू करने की तैयारी।"
    },
    {
        "id": 15, "name": "Vivaha", "name_hi": "विवाह", "purpose": "Marriage",
        "age": "Adult",
        "image": "vivaha.jpg",
        "mantra": "ॐ समञ्जन्तु विश्वेदेवाः समापो हृदयानि नौ ।",
        "desc_en": "The marriage ceremony. A sacred union.",
        "desc_hi": "विवाह संस्कार। धर्म, अर्थ और काम की पूर्ति के लिए पवित्र मिलन।"
    },
    {
        "id": 16, "name": "Antyeshti", "name_hi": "अन्त्येष्टि", "purpose": "Funeral rites", "age": "Death",
        "image": "antyeshti.jpg",
        "mantra": "ॐ वायुरनिलममृतमथेदं भस्मान्तं शरीरम् ।",
        "desc_en": "Final rites performed after death.",
        "desc_hi": "मृत्यु के बाद किए जाने वाले अंतिम संस्कार, जो आत्मा की शांति के लिए हैं।"
    }
]

# --- App Routes ---
with app.app_context():
    db.create_all()
    if not Priest.query.first():
        db.session.add_all([
            Priest(name="Pandit Sharma", specialty="Vivaha"),
            Priest(name="Pandit Joshi", specialty="General"),
            Priest(name="Pandit Vats", specialty="Antyeshti")
        ])
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html', sanskars=SANSKARS)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        data = request.form
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        available_priest = None
        all_priests = Priest.query.filter_by(is_active=True).all()
        
        for priest in all_priests:
            conflict = Booking.query.filter_by(
                priest_id=priest.id, 
                date=date_obj, 
                time_slot=data['time']
            ).first()
            if not conflict:
                available_priest = priest
                break
        
        status = "Confirmed" if available_priest else "Waitlist"
        assigned_id = available_priest.id if available_priest else None
        
        new_booking = Booking(
            client_name=data['name'],
            ceremony_type=data['ceremony'],
            date=date_obj,
            time_slot=data['time'],
            status=status,
            priest_id=assigned_id
        )
        db.session.add(new_booking)
        db.session.commit()
        
        return render_template('book.html', success=True, status=status, priest=available_priest)

    return render_template('book.html')

@app.route('/api/check_availability', methods=['POST'])
def check_availability():
    req = request.get_json()
    date_str = req.get('date')
    time_slot = req.get('time')
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        total_priests = Priest.query.count()
        busy_priests = Booking.query.filter_by(date=date_obj, time_slot=time_slot).count()
        available = total_priests - busy_priests
        return jsonify({'available': available > 0, 'slots_left': available})
    except:
        return jsonify({'available': False, 'slots_left': 0})

@app.route('/admin')
def admin():
    bookings = Booking.query.order_by(Booking.date.desc()).all()
    priests = Priest.query.all()
    return render_template('admin.html', bookings=bookings, priests=priests)

if __name__ == '__main__':
    app.run(debug=True)