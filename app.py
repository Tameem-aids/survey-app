from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # غيّر هذا المفتاح

# كلمة مرور لوحة التحكم (غيّرها)
ADMIN_PASSWORD = 'tameem7777'

DATABASE = 'survey.db'

def get_db():
    """الاتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """إنشاء جداول قاعدة البيانات"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT NOT NULL,
            age TEXT NOT NULL,
            major TEXT NOT NULL,
            major_other TEXT,
            level TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            response_id INTEGER NOT NULL,
            question_number INTEGER NOT NULL,
            answer INTEGER NOT NULL,
            dimension TEXT NOT NULL,
            FOREIGN KEY (response_id) REFERENCES responses(id)
        )
    ''')
    conn.commit()
    conn.close()

def login_required(f):
    """التحقق من تسجيل دخول المشرف"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== أسئلة الاستبيان ==========
QUESTIONS = {
    'dim1': {
        'title': 'البعد الأول: التنظيم والتخطيط في العلاقات العامة',
        'variable': 'المتغير المستقل: دور العلاقات العامة',
        'questions': [
            (1, 'توجد جهة أو وحدة واضحة في الكلية تتولى مهام العلاقات العامة.'),
            (2, 'تقوم الكلية بالتخطيط المسبق لأنشطة العلاقات العامة وبرامجها.'),
            (3, 'تعتمد الكلية على أساليب منظمة في التواصل مع الطلبة.'),
            (4, 'تتسم أنشطة العلاقات العامة في الكلية بالاستمرارية وليس بالعشوائية.'),
            (5, 'تحرص إدارة الكلية على دعم أنشطة العلاقات العامة وتفعيلها.'),
            (6, 'توجد أهداف واضحة لأنشطة العلاقات العامة في الكلية.'),
        ]
    },
    'dim2': {
        'title': 'البعد الثاني: الأنشطة الاتصالية للعلاقات العامة',
        'variable': 'المتغير المستقل: دور العلاقات العامة',
        'questions': [
            (7, 'تسهم الأنشطة الاتصالية في الكلية في تعريف الطلبة بخدمات الكلية وأنشطتها.'),
            (8, 'تقدم الكلية معلومات كافية وواضحة للطلبة عند الحاجة.'),
            (9, 'تستخدم الكلية وسائل مناسبة للإعلان عن الفعاليات والأنشطة.'),
            (10, 'تساعد الرسائل الإعلامية الصادرة عن الكلية في تكوين فهم واضح لدى الطلبة.'),
            (11, 'تتميز الأنشطة الاتصالية في الكلية بالوضوح والموضوعية.'),
            (12, 'تسهم العلاقات العامة في تعزيز التواصل بين إدارة الكلية والطلبة.'),
        ]
    },
    'dim3': {
        'title': 'البعد الثالث: الإعلام الرقمي ووسائل التواصل الاجتماعي',
        'variable': 'المتغير المستقل: دور العلاقات العامة',
        'questions': [
            (13, 'تمتلك الكلية حسابات رسمية نشطة على وسائل التواصل الاجتماعي.'),
            (14, 'تستخدم الكلية وسائل التواصل الاجتماعي في إيصال المعلومات للطلبة بفاعلية.'),
            (15, 'يتم تحديث المحتوى الرقمي للكلية بشكل منتظم.'),
            (16, 'تتيح الكلية للطلبة التفاعل والمشاركة عبر المنصات الرقمية.'),
            (17, 'تسهم وسائل التواصل الاجتماعي في تحسين صورة الكلية.'),
            (18, 'يعكس المحتوى الرقمي للكلية أنشطتها وإنجازاتها بشكل إيجابي.'),
        ]
    },
    'dim4': {
        'title': 'البعد الرابع: إدارة العلاقة مع الجمهور الداخلي',
        'variable': 'المتغير المستقل: دور العلاقات العامة',
        'questions': [
            (19, 'تسعى الكلية إلى بناء علاقات إيجابية مع الطلبة.'),
            (20, 'تستمع إدارة الكلية لآراء الطلبة واحتياجاتهم.'),
            (21, 'تهتم الكلية بمعالجة شكاوى الطلبة والرد عليها.'),
            (22, 'تشجع الكلية الطلبة على المشاركة في الأنشطة والفعاليات.'),
            (23, 'تتوفر قنوات تواصل فعالة بين إدارة الكلية والطلبة.'),
            (24, 'تحرص الكلية على خلق بيئة تعليمية داعمة ومحفزة للطلبة.'),
        ]
    },
    'dim5': {
        'title': 'البعد الخامس: المعوقات',
        'variable': 'المتغير المستقل: دور العلاقات العامة',
        'questions': [
            (25, 'يؤثر ضعف الموارد المادية سلبًا على أنشطة العلاقات العامة في الكلية.'),
            (26, 'يعاني قسم العلاقات العامة من نقص في الكوادر المؤهلة.'),
            (27, 'تؤثر البيئة الأمنية والسياسية على أداء العلاقات العامة في الكلية.'),
            (28, 'يفتقر العاملون في العلاقات العامة إلى التدريب الكافي.'),
            (29, 'تؤثر محدودية التقنيات المستخدمة على فاعلية الأنشطة الاتصالية.'),
        ]
    },
    'dim6': {
        'title': 'البعد الأول: الصورة الذهنية',
        'variable': 'المتغير التابع: السمعة المؤسسية',
        'questions': [
            (30, 'لدي انطباع إيجابي عن كلية الآداب بجامعة تعز.'),
            (31, 'تقدم الكلية صورة مهنية وأكاديمية واضحة.'),
            (32, 'أشعر بأن الكلية تمتلك هوية مؤسسية مميزة.'),
            (33, 'تعكس أنشطة الكلية صورة إيجابية لدى المجتمع المحلي.'),
        ]
    },
    'dim7': {
        'title': 'البعد الثاني: الثقة والمصداقية',
        'variable': 'المتغير التابع: السمعة المؤسسية',
        'questions': [
            (34, 'أثق في قدرة الكلية على تقديم تعليم أكاديمي جيد.'),
            (35, 'أشعر بأن الكلية تتعامل مع الطلبة بشفافية ووضوح.'),
            (36, 'تلتزم إدارة الكلية بالوعود والقرارات التي تعلن عنها.'),
            (37, 'أثق في أن الكلية تعمل لمصلحة الطلبة بالدرجة الأولى.'),
        ]
    },
    'dim8': {
        'title': 'البعد الثالث: الولاء والانتماء',
        'variable': 'المتغير التابع: السمعة المؤسسية',
        'questions': [
            (38, 'أشعر بالفخر لانتمائي إلى كلية الآداب بجامعة تعز.'),
            (39, 'أوصي الآخرين بالالتحاق بهذه الكلية.'),
            (40, 'أشعر بالارتباط العاطفي بالكلية ومجتمعها.'),
            (41, 'أحرص على المشاركة في أنشطة الكلية وفعالياتها.'),
        ]
    },
    'dim9': {
        'title': 'البعد الرابع: الحضور الأكاديمي والمجتمعي',
        'variable': 'المتغير التابع: السمعة المؤسسية',
        'questions': [
            (42, 'تسهم الكلية في خدمة المجتمع المحلي من خلال أنشطتها.'),
            (43, 'تحظى الكلية بسمعة أكاديمية جيدة مقارنة بالكليات الأخرى.'),
            (44, 'تشارك الكلية في فعاليات ومؤتمرات علمية محلية أو دولية.'),
            (45, 'تُخرّج الكلية كوادر مؤهلة تخدم سوق العمل.'),
        ]
    }
}

@app.route('/')
def index():
    """الصفحة الرئيسية - نموذج الاستبيان"""
    return render_template('survey.html', questions=QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit():
    """استلام وحفظ إجابات الاستبيان"""
    try:
        # البيانات العامة
        gender = request.form.get('gender')
        age = request.form.get('age')
        major = request.form.get('major')
        major_other = request.form.get('major_other', '')
        level = request.form.get('level')

        # التحقق من البيانات
        if not all([gender, age, major, level]):
            flash('يرجى ملء جميع البيانات العامة', 'error')
            return redirect(url_for('index'))

        # التحقق من الإجابات
        answers = []
        for dim_key, dim_data in QUESTIONS.items():
            for q_num, q_text in dim_data['questions']:
                answer = request.form.get(f'q{q_num}')
                if not answer:
                    flash(f'يرجى الإجابة على جميع العبارات (العبارة رقم {q_num})', 'error')
                    return redirect(url_for('index'))
                answers.append((q_num, int(answer), dim_data['title']))

        # حفظ في قاعدة البيانات
        conn = get_db()
        cursor = conn.execute(
            'INSERT INTO responses (gender, age, major, major_other, level) VALUES (?, ?, ?, ?, ?)',
            (gender, age, major, major_other, level)
        )
        response_id = cursor.lastrowid

        for q_num, answer, dimension in answers:
            conn.execute(
                'INSERT INTO answers (response_id, question_number, answer, dimension) VALUES (?, ?, ?, ?)',
                (response_id, q_num, answer, dimension)
            )

        conn.commit()
        conn.close()

        return render_template('thank_you.html')

    except Exception as e:
        flash(f'حدث خطأ: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """تسجيل دخول المشرف"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('كلمة المرور غير صحيحة', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """تسجيل خروج المشرف"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """لوحة التحكم"""
    conn = get_db()

    # إجمالي الاستجابات
    total = conn.execute('SELECT COUNT(*) FROM responses').fetchone()[0]

    # إحصائيات النوع
    gender_stats = conn.execute(
        'SELECT gender, COUNT(*) as count FROM responses GROUP BY gender'
    ).fetchall()

    # إحصائيات التخصص
    major_stats = conn.execute(
        'SELECT major, COUNT(*) as count FROM responses GROUP BY major'
    ).fetchall()

    # إحصائيات المستوى
    level_stats = conn.execute(
        'SELECT level, COUNT(*) as count FROM responses GROUP BY level'
    ).fetchall()

    # متوسط كل بعد
    dimension_avgs = conn.execute('''
        SELECT dimension, ROUND(AVG(answer), 2) as avg_answer
        FROM answers
        GROUP BY dimension
        ORDER BY dimension
    ''').fetchall()

    # آخر 10 استجابات
    recent = conn.execute(
        'SELECT * FROM responses ORDER BY submitted_at DESC LIMIT 10'
    ).fetchall()

    conn.close()

    return render_template('admin_dashboard.html',
        total=total,
        gender_stats=gender_stats,
        major_stats=major_stats,
        level_stats=level_stats,
        dimension_avgs=dimension_avgs,
        recent=recent
    )

@app.route('/admin/export')
@login_required
def export_csv():
    """تصدير البيانات كملف CSV"""
    import csv
    import io

    conn = get_db()
    responses = conn.execute('SELECT * FROM responses ORDER BY id').fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    # رأس الجدول
    header = ['رقم', 'النوع', 'العمر', 'التخصص', 'تخصص آخر', 'المستوى', 'تاريخ التقديم']
    for i in range(1, 46):
        header.append(f'س{i}')
    writer.writerow(header)

    # البيانات
    for resp in responses:
        row = [resp['id'], resp['gender'], resp['age'], resp['major'],
               resp['major_other'], resp['level'], resp['submitted_at']]

        answers = conn.execute(
            'SELECT question_number, answer FROM answers WHERE response_id = ? ORDER BY question_number',
            (resp['id'],)
        ).fetchall()

        answer_dict = {a['question_number']: a['answer'] for a in answers}
        for i in range(1, 46):
            row.append(answer_dict.get(i, ''))

        writer.writerow(row)

    conn.close()

    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=survey_results.csv'}
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
