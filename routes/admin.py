from flask import Blueprint, jsonify, Response, render_template, session, redirect, url_for
from models import Campaign
import csv
import io

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create',methods=['GET'])
def create_page():
    if not session.get('logged_in'):
        return redirect((url_for('index')))
    return render_template('create_campaign.html')

@admin_bp.route('/admin/campaigns', methods=['GET'])
def list_campaigns():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    campaigns = Campaign.query.all()
    data = [{
        'id': c.id,
        'name': c.name,
        'target_email': c.target_email,
        'subject': c.subject,
        'sent': c.sent,
        'opened': c.opened,
        'clicked': c.clicked,
        'submitted': c.submitted
    } for c in campaigns]
    return jsonify(data)


@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))  # redirect to login if not authenticated

    campaigns = Campaign.query.all()
    return render_template('admin_dashboard.html', campaigns=campaigns)

@admin_bp.route('/admin/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    campaign = Campaign.query.get_or_404(campaign_id)
    return jsonify({
        'id': campaign.id,
        'name': campaign.name,
        'target_email': campaign.target_email,
        'subject': campaign.subject,
        'body': campaign.body,
        'sent': campaign.sent,
        'opened': campaign.opened,
        'clicked': campaign.clicked,
        'submitted': campaign.submitted,
        'username_submitted' : campaign.submitted_username,
        'password_submitted' : campaign.submitted_password
    })

@admin_bp.route('/admin/export', methods=['GET'])
def export_csv():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    campaigns = Campaign.query.all()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['ID', 'Name', 'Target Email', 'Subject', 'Sent', 'Opened', 'Clicked', 'Submitted'])
    for c in campaigns:
        writer.writerow([
            c.id, c.name, c.target_email, c.subject,
            c.sent, c.opened, c.clicked, c.submitted
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=phishing_campaigns.csv'
    return response

@admin_bp.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))
