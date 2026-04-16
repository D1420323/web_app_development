from flask import render_template, request, redirect, url_for, flash, session
from . import recipe_bp
from ..models.recipe import Recipe
from ..models.ingredient import Ingredient
from ..models.recipe_step import RecipeStep

def get_current_user_id():
    """輔助函式：取得當前登入使用者的 ID"""
    return session.get('user_id')

@recipe_bp.route('/')
def dashboard():
    """
    HTTP Method: GET
    顯示當前使用者的「個人食譜面板」，列出自己收藏/建立的食譜。
    Template: recipe/dashboard.html
    """
    user_id = get_current_user_id()
    if not user_id:
        flash('請先登入後才能檢視食譜面板', 'warning')
        return redirect(url_for('auth.login'))
    
    # 根據作者抓取食譜清單
    recipes = Recipe.query.filter_by(user_id=user_id).order_by(Recipe.created_at.desc()).all()
    return render_template('recipe/dashboard.html', recipes=recipes)

@recipe_bp.route('/<int:id>')
def detail(id):
    """
    HTTP Method: GET
    顯示單一食譜的詳細內容 (包含食材、步驟)。前端會處理份量動態換算。
    Template: recipe/detail.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('main.index'))
        
    return render_template('recipe/detail.html', recipe=recipe)

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    HTTP Method: GET, POST
    GET: 顯示新增食譜的表單。 (Template: recipe/new.html)
    POST: 接收表單資料，寫入相關資料表 (Recipe, Ingredient, RecipeStep) 後重導至該食譜詳情頁。
    """
    user_id = get_current_user_id()
    if not user_id:
        flash('操作前請先登入', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        default_portions = request.form.get('default_portions', 1)

        # 簡單驗證
        if not title:
            flash('食譜名稱為必填項目！', 'danger')
            return render_template('recipe/new.html')

        try:
            portions = int(default_portions)
        except ValueError:
            portions = 1

        # 新增 Recipe
        recipe_data = {
            'user_id': user_id,
            'title': title,
            'description': description,
            'default_portions': portions
        }
        new_recipe = Recipe.create(recipe_data)

        if new_recipe:
            # 處理可能的多個食材 (假設前端表單傳送 ing_name[] 等 array)
            # 這邊為示意，需與後續 template name 屬性對應
            ing_names = request.form.getlist('ing_name[]')
            ing_quants = request.form.getlist('ing_quantity[]')
            ing_units = request.form.getlist('ing_unit[]')
            
            for i in range(len(ing_names)):
                if ing_names[i].strip():
                    try:
                        q = float(ing_quants[i]) if ing_quants[i] else 0.0
                    except ValueError:
                        q = 0.0
                    Ingredient.create({
                        'recipe_id': new_recipe.id,
                        'name': ing_names[i].strip(),
                        'quantity': q,
                        'unit': ing_units[i] if i < len(ing_units) else ''
                    })
            
            # 處理詳細步驟
            step_instructions = request.form.getlist('step_instruction[]')
            for i, instruction in enumerate(step_instructions):
                if instruction.strip():
                    RecipeStep.create({
                        'recipe_id': new_recipe.id,
                        'step_number': i + 1,
                        'instruction': instruction.strip()
                    })

            flash('新增食譜成功！', 'success')
            return redirect(url_for('recipe.detail', id=new_recipe.id))
        else:
            flash('新增失敗，這可能是系統錯誤。', 'danger')

    return render_template('recipe/new.html')

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    HTTP Method: GET, POST
    GET: 載入舊食譜資料顯示於編輯表單。 (Template: recipe/edit.html)
    POST: 接收更新的表單資料，更新資料表後重導至該食譜詳情頁。
    """
    user_id = get_current_user_id()
    recipe = Recipe.get_by_id(id)

    if not recipe:
        flash('找不到要編輯的食譜！', 'danger')
        return redirect(url_for('recipe.dashboard'))

    # 作者權限驗證
    if recipe.user_id != user_id:
        flash('您無權編輯此篇食譜。', 'danger')
        return redirect(url_for('recipe.detail', id=id))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        default_portions = request.form.get('default_portions', recipe.default_portions)

        if not title:
            flash('食譜標題為必填項目！', 'danger')
            return render_template('recipe/edit.html', recipe=recipe)
            
        try:
            portions = int(default_portions)
        except ValueError:
            portions = recipe.default_portions

        update_data = {
            'title': title,
            'description': description,
            'default_portions': portions
        }

        if recipe.update(update_data):
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe.id))
        else:
            flash('食譜更新失敗。', 'danger')

    return render_template('recipe/edit.html', recipe=recipe)

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    HTTP Method: POST
    刪除指定 ID 的食譜，刪除後重導向至個人面板。
    （需驗證是否為作者本人操作）
    """
    user_id = get_current_user_id()
    recipe = Recipe.get_by_id(id)

    if not recipe:
        flash('找不到要刪除的食譜。', 'danger')
        return redirect(url_for('recipe.dashboard'))

    if recipe.user_id != user_id:
        flash('您無權刪除此篇食譜。', 'danger')
        return redirect(url_for('recipe.detail', id=id))

    if recipe.delete():
        flash(f'食譜 "{recipe.title}" 刪除成功。', 'success')
    else:
        flash('發生錯誤，無法刪除食譜。', 'danger')

    return redirect(url_for('recipe.dashboard'))
