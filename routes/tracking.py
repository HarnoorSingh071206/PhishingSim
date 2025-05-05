from flask import Blueprint, request, send_file
from models import Campaign, db
from flask import render_template

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track/open/<int:campaign_id>')
def track_open(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    campaign.opened = True
    db.session.commit()
    return send_file('static/pixel.png', mimetype='image/png')

@tracking_bp.route('/fake_login/<int:campaign_id>')
def fake_login(campaign_id):
    return render_template('fake_login.html', campaign_id=campaign_id)

@tracking_bp.route('/track/click/<int:campaign_id>')
def track_click(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    campaign.clicked = True
    db.session.commit()
    return "<h3>You were part of a phishing test.</h3>"

@tracking_bp.route('/track/submit/<int:campaign_id>', methods=['POST'])
def track_submit(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    campaign.submitted = True
    campaign.submitted_username = request.form.get('username')
    campaign.submitted_password = request.form.get('password')

    db.session.commit()

    print("Captured (simulated):", campaign.submitted_username, campaign.submitted_password)

    return "<h3>Thank you for participating in this awareness exercise.</h3>"
