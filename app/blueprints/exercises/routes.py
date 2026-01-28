from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.blueprints.exercises import bp
from app import db
from app.models import (
    User, Competition, Exercise, ExercisePointEntry, 
    ExerciseResult, Starter, CompetitionResult
)
from app.decorators import roles_required


# ==================== WT EXERCISES PAGE ====================
@bp.route('/wt/<int:competition_id>')
@login_required
def wt_exercises(competition_id):
    """Display all exercises for a working test.
    
    - Admins and organizers see all exercises with edit/delete options
    - Helpers see only their assigned exercises
    - Visitors cannot access this page
    """
    competition = Competition.query.get_or_404(competition_id)
    
    # Determine which exercises to show based on role
    if current_user.role in ['admin', 'organizer']:
        exercises = Exercise.query.filter_by(competition_id=competition_id).all()
    elif current_user.role == 'helper':
        exercises = Exercise.query.filter_by(
            competition_id=competition_id,
            helper_id=current_user.id
        ).all()
    else:
        # Visitors are not allowed to see this page
        abort(403)
    
    return render_template(
        'wt_exercises.html.jinja',
        competition=competition,
        exercises=exercises
    )


@bp.route('/add/<int:competition_id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'organizer'])
def add_exercise(competition_id):
    """Add a new exercise to a working test."""
    competition = Competition.query.get_or_404(competition_id)
    
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        max_points = request.form.get('max_points', 100, type=int)
        judge_id = request.form.get('judge_id', type=int) or None
        helper_id = request.form.get('helper_id', type=int) or None
        
        if not name:
            flash('Exercise name is required.', 'danger')
            return render_template('add_exercise.html.jinja', competition=competition, users=User.query.all())
        
        # Validate users exist if assigned
        if judge_id and not User.query.get(judge_id):
            flash('Selected judge does not exist.', 'danger')
            return render_template('add_exercise.html.jinja', competition=competition, users=User.query.all())
        
        if helper_id and not User.query.get(helper_id):
            flash('Selected helper does not exist.', 'danger')
            return render_template('add_exercise.html.jinja', competition=competition, users=User.query.all())
        
        exercise = Exercise(
            name=name,
            competition_id=competition_id,
            max_points=max_points,
            judge_id=judge_id,
            helper_id=helper_id
        )
        
        db.session.add(exercise)
        db.session.commit()
        
        flash(f'Exercise "{name}" added successfully.', 'success')
        return redirect(url_for('exercises.wt_exercises', competition_id=competition_id))
    
    users = User.query.all()
    return render_template('add_exercise.html.jinja', competition=competition, users=users)


@bp.route('/edit/<int:exercise_id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'organizer'])
def edit_exercise(exercise_id):
    """Edit an exercise."""
    exercise = Exercise.query.get_or_404(exercise_id)
    
    if request.method == 'POST':
        exercise.name = (request.form.get('name') or '').strip()
        exercise.max_points = request.form.get('max_points', exercise.max_points, type=int)
        exercise.judge_id = request.form.get('judge_id', type=int) or None
        exercise.helper_id = request.form.get('helper_id', type=int) or None
        
        if not exercise.name:
            flash('Exercise name is required.', 'danger')
            return redirect(url_for('exercises.edit_exercise', exercise_id=exercise_id))
        
        db.session.commit()
        flash('Exercise updated successfully.', 'success')
        return redirect(url_for('exercises.wt_exercises', competition_id=exercise.competition_id))
    
    users = User.query.all()
    return render_template('edit_exercise.html.jinja', exercise=exercise, users=users)


@bp.route('/delete/<int:exercise_id>', methods=['POST'])
@login_required
@roles_required(['admin', 'organizer'])
def delete_exercise(exercise_id):
    """Delete an exercise."""
    exercise = Exercise.query.get_or_404(exercise_id)
    competition_id = exercise.competition_id
    
    # Delete all related point entries and results
    ExercisePointEntry.query.filter_by(exercise_id=exercise_id).delete()
    ExerciseResult.query.filter_by(exercise_id=exercise_id).delete()
    
    db.session.delete(exercise)
    db.session.commit()
    
    flash('Exercise deleted successfully.', 'success')
    return redirect(url_for('exercises.wt_exercises', competition_id=competition_id))


# ==================== EXERCISE POINT ENTRY PAGE ====================
@bp.route('/point-entry/<int:exercise_id>', methods=['GET', 'POST'])
@login_required
def exercise_point_entry(exercise_id):
    """Enter points for an exercise.
    
    - Only helpers assigned to the exercise can enter points
    - Organizers and admins have full access
    """
    exercise = Exercise.query.get_or_404(exercise_id)
    
    # Check authorization
    if not (current_user.role in ['admin', 'organizer'] or 
            current_user.id == exercise.helper_id):
        abort(403)
    
    # Get all starters for this competition
    starters = Starter.query.filter_by(competition_id=exercise.competition_id).all()
    
    if request.method == 'POST':
        for starter in starters:
            points_input = request.form.get(f'points_{starter.id}')
            notes = request.form.get(f'notes_{starter.id}', '').strip()
            
            if points_input:
                try:
                    points = int(points_input)
                    
                    if points < 0 or points > exercise.max_points:
                        flash(f'Points must be between 0 and {exercise.max_points}.', 'danger')
                        continue
                    
                    # Update or create point entry
                    entry = ExercisePointEntry.query.filter_by(
                        exercise_id=exercise_id,
                        starter_id=starter.id
                    ).first()
                    
                    if entry:
                        entry.points = points
                        entry.notes = notes
                    else:
                        entry = ExercisePointEntry(
                            exercise_id=exercise_id,
                            starter_id=starter.id,
                            points=points,
                            notes=notes
                        )
                        db.session.add(entry)
                
                except ValueError:
                    flash(f'Invalid points value for {starter.id}.', 'danger')
        
        db.session.commit()
        flash('Points saved successfully.', 'success')
        return redirect(url_for('exercises.exercise_point_entry', exercise_id=exercise_id))
    
    # Get existing point entries
    point_entries = {
        pe.starter_id: pe 
        for pe in ExercisePointEntry.query.filter_by(exercise_id=exercise_id).all()
    }
    
    return render_template(
        'exercise_point_entry.html.jinja',
        exercise=exercise,
        starters=starters,
        point_entries=point_entries
    )


# ==================== RESULTS PAGE ====================
@bp.route('/results/<int:competition_id>')
def competition_results(competition_id):
    """Display final results of a working test.
    
    - Admin/Organizer: Always see full results page with publish/unpublish options
    - Helper/Visitor: Can see results if published, otherwise "No results available yet"
    """
    competition = Competition.query.get_or_404(competition_id)
    
    exercises = Exercise.query.filter_by(competition_id=competition_id).all()
    starters = Starter.query.filter_by(competition_id=competition_id).all()
    
    # Get or create competition result status
    result_status = CompetitionResult.query.filter_by(
        competition_id=competition_id
    ).first()
    
    if not result_status:
        result_status = CompetitionResult(competition_id=competition_id)
        db.session.add(result_status)
        db.session.commit()
    
    # Check if user is admin/organizer
    is_admin_or_organizer = (
        current_user.is_authenticated and 
        current_user.role in ['admin', 'organizer']
    )
    
    # For non-admins: only show results if published
    if not is_admin_or_organizer and not result_status.published:
        starter_results = {}
    else:
        # Calculate results for each starter
        starter_results = {}
        for starter in starters:
            total_points = 0
            exercise_scores = {}
            
            for exercise in exercises:
                point_entry = ExercisePointEntry.query.filter_by(
                    exercise_id=exercise.id,
                    starter_id=starter.id
                ).first()
                
                if point_entry:
                    exercise_scores[exercise.id] = point_entry.points
                    total_points += point_entry.points
                else:
                    exercise_scores[exercise.id] = None
            
            starter_results[starter.id] = {
                'starter': starter,
                'exercise_scores': exercise_scores,
                'total_points': total_points
            }
    
    return render_template(
        'competition_results.html.jinja',
        competition=competition,
        exercises=exercises,
        starter_results=starter_results,
        result_status=result_status,
        is_admin_or_organizer=is_admin_or_organizer
    )


@bp.route('/publish/<int:competition_id>', methods=['POST'])
@login_required
@roles_required(['admin', 'organizer'])
def publish_results(competition_id):
    """Publish results for a working test."""
    competition = Competition.query.get_or_404(competition_id)
    
    result_status = CompetitionResult.query.filter_by(
        competition_id=competition_id
    ).first()
    
    if not result_status:
        result_status = CompetitionResult(competition_id=competition_id)
        db.session.add(result_status)
    
    result_status.published = True
    from datetime import datetime
    result_status.published_at = datetime.now()
    
    db.session.commit()
    
    flash('Results published successfully. Visitors can now view the results.', 'success')
    return redirect(url_for('exercises.competition_results', competition_id=competition_id))


@bp.route('/unpublish/<int:competition_id>', methods=['POST'])
@login_required
@roles_required(['admin', 'organizer'])
def unpublish_results(competition_id):
    """Unpublish results for a working test."""
    competition = Competition.query.get_or_404(competition_id)
    
    result_status = CompetitionResult.query.filter_by(
        competition_id=competition_id
    ).first()
    
    if result_status:
        result_status.published = False
        db.session.commit()
    
    flash('Results unpublished.', 'success')
    return redirect(url_for('exercises.competition_results', competition_id=competition_id))
