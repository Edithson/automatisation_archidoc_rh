from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem

# ── Couleurs ──────────────────────────────────────────────────────────────
KOTLIN_PURPLE   = colors.HexColor('#7F52FF')
ANDROID_GREEN   = colors.HexColor('#3DDC84')
DARK_BG         = colors.HexColor('#1E1E2E')
CODE_BG         = colors.HexColor('#F4F4F8')
ACCENT          = colors.HexColor('#FF6B35')
TEXT_DARK       = colors.HexColor('#1A1A2E')
LIGHT_PURPLE    = colors.HexColor('#EDE7FF')
LIGHT_GREEN     = colors.HexColor('#E8F9F0')
GREY_TEXT       = colors.HexColor('#555577')

PAGE_W, PAGE_H  = A4
MARGIN          = 2 * cm

# ── Styles ────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

cover_title = S('CoverTitle',
    fontName='Helvetica-Bold', fontSize=42, textColor=colors.white,
    alignment=TA_CENTER, spaceAfter=10, leading=50)

cover_sub = S('CoverSub',
    fontName='Helvetica', fontSize=18, textColor=ANDROID_GREEN,
    alignment=TA_CENTER, spaceAfter=6, leading=26)

cover_author = S('CoverAuthor',
    fontName='Helvetica-Oblique', fontSize=13, textColor=colors.HexColor('#CCCCEE'),
    alignment=TA_CENTER, spaceAfter=4)

ch_num = S('ChNum',
    fontName='Helvetica-Bold', fontSize=13, textColor=KOTLIN_PURPLE,
    alignment=TA_LEFT, spaceBefore=30, spaceAfter=4)

ch_title = S('ChTitle',
    fontName='Helvetica-Bold', fontSize=28, textColor=TEXT_DARK,
    alignment=TA_LEFT, spaceBefore=4, spaceAfter=16, leading=34)

section = S('Section',
    fontName='Helvetica-Bold', fontSize=16, textColor=KOTLIN_PURPLE,
    spaceBefore=20, spaceAfter=8, leading=20)

subsection = S('Subsection',
    fontName='Helvetica-Bold', fontSize=13, textColor=TEXT_DARK,
    spaceBefore=14, spaceAfter=6)

body = S('Body',
    fontName='Helvetica', fontSize=11, textColor=TEXT_DARK,
    alignment=TA_JUSTIFY, spaceBefore=4, spaceAfter=6, leading=17)

code_style = S('Code',
    fontName='Courier', fontSize=9, textColor=colors.HexColor('#2D2D5E'),
    backColor=CODE_BG, spaceBefore=8, spaceAfter=8, leading=14,
    leftIndent=12, rightIndent=12, borderPadding=(6,6,6,6))

tip_style = S('Tip',
    fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1A4A2E'),
    backColor=LIGHT_GREEN, spaceBefore=8, spaceAfter=8, leading=15,
    leftIndent=12, rightIndent=12, borderPadding=(6,6,6,6))

warn_style = S('Warn',
    fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#4A1A00'),
    backColor=colors.HexColor('#FFF3E0'), spaceBefore=8, spaceAfter=8, leading=15,
    leftIndent=12, rightIndent=12, borderPadding=(6,6,6,6))

toc_title = S('TocTitle',
    fontName='Helvetica-Bold', fontSize=22, textColor=TEXT_DARK,
    alignment=TA_CENTER, spaceAfter=24)

toc_ch = S('TocCh',
    fontName='Helvetica-Bold', fontSize=12, textColor=KOTLIN_PURPLE,
    spaceBefore=8, spaceAfter=2)

toc_item = S('TocItem',
    fontName='Helvetica', fontSize=10, textColor=GREY_TEXT,
    leftIndent=16, spaceAfter=1)

caption = S('Caption',
    fontName='Helvetica-Oblique', fontSize=9, textColor=GREY_TEXT,
    alignment=TA_CENTER, spaceAfter=10)

# ── Helpers ───────────────────────────────────────────────────────────────
def HR(color=KOTLIN_PURPLE, thickness=1.5):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=8, spaceBefore=4)

def code(text):
    safe = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return Paragraph(safe, code_style)

def tip(text):
    return Paragraph(f"<b>💡 Astuce :</b> {text}", tip_style)

def warn(text):
    return Paragraph(f"<b>⚠️ Attention :</b> {text}", warn_style)

def info_box(title, text, bg=LIGHT_PURPLE):
    style = S('InfoBox', fontName='Helvetica', fontSize=10,
              textColor=TEXT_DARK, backColor=bg, leading=15,
              leftIndent=12, rightIndent=12, borderPadding=(6,6,6,6),
              spaceBefore=8, spaceAfter=8)
    title_style = S('InfoTitle', fontName='Helvetica-Bold', fontSize=10,
                    textColor=KOTLIN_PURPLE, backColor=bg, leading=15,
                    leftIndent=12, rightIndent=12, borderPadding=(6,2,0,6))
    return [Paragraph(f"<b>📌 {title}</b>", title_style), Paragraph(text, style)]

# ── Générateur de page de couverture ─────────────────────────────────────
class CoverPage:
    def __init__(self):
        pass
    def build(self, canvas, doc):
        canvas.saveState()
        # Fond dégradé simulé
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # Bande couleur en haut
        canvas.setFillColor(KOTLIN_PURPLE)
        canvas.rect(0, PAGE_H - 3*cm, PAGE_W, 3*cm, fill=1, stroke=0)
        # Bande verte en bas
        canvas.setFillColor(ANDROID_GREEN)
        canvas.rect(0, 0, PAGE_W, 1.2*cm, fill=1, stroke=0)
        # Décorations cercles
        canvas.setFillColor(colors.HexColor('#2A2A4A'))
        canvas.circle(PAGE_W - 3*cm, PAGE_H/2, 5*cm, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor('#25253A'))
        canvas.circle(2*cm, PAGE_H/2 - 4*cm, 3.5*cm, fill=1, stroke=0)
        canvas.restoreState()

def on_page(canvas, doc):
    canvas.saveState()
    # En-tête
    canvas.setFillColor(KOTLIN_PURPLE)
    canvas.rect(0, PAGE_H - 1*cm, PAGE_W, 1*cm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.white)
    canvas.drawString(MARGIN, PAGE_H - 0.65*cm, "Développement Android avec Kotlin")
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.65*cm, "Guide Pratique Complet")
    # Pied de page
    canvas.setFillColor(CODE_BG)
    canvas.rect(0, 0, PAGE_W, 0.9*cm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawCentredString(PAGE_W/2, 0.3*cm, f"— {doc.page} —")
    canvas.restoreState()

# ══════════════════════════════════════════════════════════════════════════
#  CONTENU DU LIVRE
# ══════════════════════════════════════════════════════════════════════════
def build_story():
    story = []

    # ── PAGE DE COUVERTURE ────────────────────────────────────────────────
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("Développement Android", cover_title))
    story.append(Paragraph("avec Kotlin", S('CT2', fontName='Helvetica-Bold',
        fontSize=42, textColor=ANDROID_GREEN, alignment=TA_CENTER, spaceAfter=16, leading=50)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Guide Pratique Complet", cover_sub))
    story.append(Paragraph("UI · Architecture MVVM · API REST · Jetpack", cover_author))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Projet fil rouge : Application TaskFlow", S('PFR',
        fontName='Helvetica-BoldOblique', fontSize=14, textColor=colors.HexColor('#FFCC66'),
        alignment=TA_CENTER)))
    story.append(Spacer(1, 6*cm))
    story.append(Paragraph("Niveau : Bases acquises → Intermédiaire/Avancé", cover_author))
    story.append(Paragraph("Édition 2025 — Kotlin 2.x · Android API 35", cover_author))
    story.append(PageBreak())

    # ── TABLE DES MATIÈRES ───────────────────────────────────────────────
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Table des matières", toc_title))
    story.append(HR(KOTLIN_PURPLE, 2))
    story.append(Spacer(1, 0.3*cm))

    toc_data = [
        ("Introduction", ["Présentation du projet TaskFlow", "Prérequis & setup"]),
        ("Chapitre 1 : Kotlin Essentiel pour Android", ["Null Safety & Smart Casts", "Data Classes & Sealed Classes", "Coroutines & Flow", "Extension Functions"]),
        ("Chapitre 2 : UI avec XML Layouts", ["Hiérarchie des vues", "ConstraintLayout avancé", "RecyclerView & Adapter", "Responsive Design (portrait/paysage)"]),
        ("Chapitre 3 : Jetpack Compose", ["Composables & Recomposition", "State & remember", "Navigation Compose", "Thème Material 3"]),
        ("Chapitre 4 : Architecture MVVM", ["ViewModel & LiveData", "Repository Pattern", "Dependency Injection (Hilt)", "Clean Architecture"]),
        ("Chapitre 5 : Persistance avec Room", ["Entités & DAO", "Database & Migrations", "Relations entre entités", "Flow avec Room"]),
        ("Chapitre 6 : API REST & Réseau", ["Retrofit & OkHttp", "Coroutines & suspend functions", "Gestion d'erreurs & Result", "Intercepteurs & Auth"]),
        ("Chapitre 7 : Navigation & Deep Links", ["Navigation Component", "Arguments entre fragments", "Deep Links & Back Stack"]),
        ("Chapitre 8 : Projet TaskFlow Complet", ["Architecture finale", "Code complet", "Tests unitaires"]),
        ("Conclusion & Prochaines Étapes", []),
    ]

    for ch, items in toc_data:
        story.append(Paragraph(ch, toc_ch))
        for item in items:
            story.append(Paragraph(f"• {item}", toc_item))

    story.append(PageBreak())

    # ── INTRODUCTION ──────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("INTRODUCTION", ch_num))
    story.append(Paragraph("Bienvenue dans le développement Android moderne", ch_title))
    story.append(HR())

    story.append(Paragraph(
        "Ce livre t'accompagne pas-à-pas dans la création d'une application Android complète "
        "appelée <b>TaskFlow</b> — un gestionnaire de tâches connecté à une API REST. "
        "À travers ce projet fil rouge, tu maîtriseras l'UI en XML et Compose, "
        "l'architecture MVVM, la persistance locale avec Room, et les appels réseau avec Retrofit.", body))

    story.append(Paragraph("Le projet TaskFlow", section))
    story.append(Paragraph(
        "TaskFlow est une application de gestion de tâches professionnelle avec :", body))

    features = [
        "Liste de tâches avec filtres et recherche",
        "Création / édition / suppression de tâches",
        "Synchronisation avec une API REST (JSONPlaceholder)",
        "Persistance locale hors-ligne avec Room",
        "Navigation multi-écrans avec Jetpack Navigation",
        "Thème clair/sombre avec Material Design 3",
    ]
    for f in features:
        story.append(Paragraph(f"  ➤  {f}", S('FItem', fontName='Helvetica', fontSize=11,
            textColor=TEXT_DARK, leftIndent=20, spaceAfter=3)))

    story.append(Paragraph("Prérequis", section))
    story.append(Paragraph(
        "Ce livre suppose que tu connais les bases de Kotlin et Android : tu sais créer une Activity, "
        "déclarer des vues en XML, et lancer une application sur un device. "
        "Si tu as suivi les chapitres précédents de ce guide, tu es parfaitement prêt.", body))

    story.append(Spacer(1, 0.3*cm))
    deps = [
        ["Dépendance", "Version", "Usage"],
        ["Kotlin", "2.0+", "Langage principal"],
        ["Android Gradle Plugin", "8.x", "Build system"],
        ["Jetpack Compose BOM", "2024.09+", "UI déclarative"],
        ["Room", "2.6+", "Base de données locale"],
        ["Retrofit", "2.11+", "Appels API REST"],
        ["Hilt", "2.51+", "Injection de dépendances"],
        ["Navigation Compose", "2.8+", "Navigation"],
        ["Coroutines", "1.8+", "Asynchronisme"],
    ]
    t = Table(deps, colWidths=[5*cm, 3*cm, 8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), KOTLIN_PURPLE),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CODE_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCDD')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    story.append(t)
    story.append(Paragraph("Tableau 0.1 — Dépendances du projet TaskFlow", caption))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 1 : KOTLIN ESSENTIEL
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 1", ch_num))
    story.append(Paragraph("Kotlin Essentiel pour Android", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Avant de plonger dans l'UI et l'architecture, consolidons les fondations Kotlin "
        "qui seront utilisées tout au long du projet TaskFlow. Ce chapitre couvre les "
        "fonctionnalités du langage indispensables à un développement Android moderne.", body))

    # 1.1 Null Safety
    story.append(Paragraph("1.1 — Null Safety & Smart Casts", section))
    story.append(Paragraph(
        "Kotlin élimine les NullPointerException grâce à son système de types. "
        "Chaque variable est soit nullable (suffixe <b>?</b>) soit non-nullable par défaut.", body))
    story.append(code(
"""// Variable non-nullable : ne peut jamais être null
var taskName: String = "Faire les courses"

// Variable nullable : peut être null
var description: String? = null

// Opérateur safe-call ?.
val length = description?.length  // null si description == null

// Opérateur Elvis ?: (valeur par défaut)
val display = description ?: "Pas de description"

// Smart Cast : après vérification, le type est automatiquement casté
fun printLength(s: String?) {
    if (s != null) {
        println(s.length)  // s est automatiquement String ici
    }
}

// Opérateur !! (à éviter - lance une exception si null)
val forced = description!!.length  // DANGER : NullPointerException si null"""))

    story.append(tip("Utilise l'opérateur Elvis ?: dans les ViewModel pour fournir des valeurs par défaut "
                     "aux données venant de la base de données ou du réseau."))

    # 1.2 Data Classes
    story.append(Paragraph("1.2 — Data Classes & Sealed Classes", section))
    story.append(Paragraph(
        "Les <b>data classes</b> sont parfaites pour modéliser les données de l'application. "
        "Kotlin génère automatiquement equals(), hashCode(), toString() et copy().", body))
    story.append(code(
"""// Data class pour notre entité Task
data class Task(
    val id: Int = 0,
    val title: String,
    val description: String = "",
    val isCompleted: Boolean = false,
    val priority: Priority = Priority.MEDIUM,
    val createdAt: Long = System.currentTimeMillis()
)

// Enum class pour la priorité
enum class Priority { LOW, MEDIUM, HIGH }

// Utilisation du copy() - immuabilité
val original = Task(title = "Apprendre Kotlin")
val completed = original.copy(isCompleted = true)

// Sealed class pour les états UI (très utilisé en MVVM)
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

// Utilisation avec when (exhaustif)
fun handleState(state: UiState<List<Task>>) = when (state) {
    is UiState.Loading  -> showLoader()
    is UiState.Success  -> showTasks(state.data)
    is UiState.Error    -> showError(state.message)
}"""))

    # 1.3 Coroutines
    story.append(Paragraph("1.3 — Coroutines & Flow", section))
    story.append(Paragraph(
        "Les Coroutines Kotlin remplacent les callbacks et AsyncTask pour la gestion "
        "de l'asynchronisme. <b>Flow</b> est la version réactive des coroutines, "
        "idéale pour observer des données qui changent dans le temps.", body))
    story.append(code(
"""// suspend function : peut être suspendue sans bloquer le thread
suspend fun fetchTasks(): List<Task> {
    delay(1000)  // Simule un appel réseau (non bloquant)
    return listOf(Task(title = "Tâche 1"), Task(title = "Tâche 2"))
}

// Lancer une coroutine dans un ViewModel
class TaskViewModel : ViewModel() {
    private val _tasks = MutableStateFlow<List<Task>>(emptyList())
    val tasks: StateFlow<List<Task>> = _tasks.asStateFlow()

    init {
        loadTasks()
    }

    private fun loadTasks() {
        viewModelScope.launch {          // Scope lié au cycle de vie du VM
            try {
                val result = fetchTasks()  // suspend function appelée ici
                _tasks.value = result
            } catch (e: Exception) {
                // Gestion d'erreur
            }
        }
    }
}

// Flow : stream de données réactif
fun observeTasksFromDb(): Flow<List<Task>> = flow {
    while (true) {
        emit(database.getAllTasks())  // Émet de nouvelles valeurs
        delay(5000)
    }
}

// Collecte d'un Flow dans un composable Compose
@Composable
fun TaskScreen(viewModel: TaskViewModel = hiltViewModel()) {
    val tasks by viewModel.tasks.collectAsStateWithLifecycle()
    // ...
}"""))

    story.append(tip("Utilise toujours viewModelScope.launch dans le ViewModel, "
                     "et lifecycleScope.launch dans les Activities/Fragments. "
                     "Ne lance jamais de coroutines dans GlobalScope en production."))

    # 1.4 Extension Functions
    story.append(Paragraph("1.4 — Extension Functions & Lambdas", section))
    story.append(Paragraph(
        "Les fonctions d'extension permettent d'ajouter des méthodes à des classes existantes "
        "sans les modifier. C'est l'une des fonctionnalités les plus puissantes de Kotlin.", body))
    story.append(code(
"""// Extension sur String
fun String.capitalize(): String =
    if (isEmpty()) this else this[0].uppercaseChar() + substring(1)

// Extension sur View (très utile pour l'UI Android)
fun View.show() { visibility = View.VISIBLE }
fun View.hide() { visibility = View.GONE }
fun View.invisible() { visibility = View.INVISIBLE }

// Extension avec lambda (pattern Builder)
fun Context.toast(message: String, duration: Int = Toast.LENGTH_SHORT) {
    Toast.makeText(this, message, duration).show()
}

// Utilisation dans une Activity
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        toast("Bienvenue dans TaskFlow !")
        myButton.hide()
    }
}

// Lambda avec receiver : scope functions
val task = Task(title = "Nouvelle tâche").apply {
    // 'this' est l'objet Task ici
}

// let, run, with, apply, also
tasks.filter { it.isCompleted }
     .map { it.title }
     .also { println("Tâches complétées : $it") }"""))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 2 : UI XML LAYOUTS
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 2", ch_num))
    story.append(Paragraph("UI avec XML Layouts", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Bien que Jetpack Compose prenne de l'ampleur, la maîtrise des layouts XML reste "
        "indispensable pour maintenir des projets existants et comprendre les fondamentaux. "
        "Ce chapitre couvre le ConstraintLayout, le RecyclerView et le responsive design.", body))

    story.append(Paragraph("2.1 — ConstraintLayout Avancé", section))
    story.append(Paragraph(
        "Le ConstraintLayout est le layout recommandé pour les UIs complexes. "
        "Il permet de positionner les vues les unes par rapport aux autres avec des contraintes, "
        "évitant les hiérarchies imbriquées qui nuisent aux performances.", body))
    story.append(code(
"""<!-- res/layout/item_task.xml -->
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="16dp">

    <!-- Checkbox à gauche -->
    <CheckBox
        android:id="@+id/checkboxCompleted"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

    <!-- Titre de la tâche -->
    <TextView
        android:id="@+id/textTitle"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="12dp"
        android:layout_marginEnd="8dp"
        android:textSize="16sp"
        android:textStyle="bold"
        app:layout_constraintStart_toEndOf="@id/checkboxCompleted"
        app:layout_constraintEnd_toStartOf="@id/chipPriority"
        app:layout_constraintTop_toTopOf="parent" />

    <!-- Description -->
    <TextView
        android:id="@+id/textDescription"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="4dp"
        android:textSize="13sp"
        android:textColor="@color/grey"
        app:layout_constraintStart_toStartOf="@id/textTitle"
        app:layout_constraintEnd_toStartOf="@id/chipPriority"
        app:layout_constraintTop_toBottomOf="@id/textTitle" />

    <!-- Chip priorité à droite -->
    <com.google.android.material.chip.Chip
        android:id="@+id/chipPriority"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>"""))

    story.append(Paragraph("2.2 — RecyclerView & ViewHolder Pattern", section))
    story.append(Paragraph(
        "Le RecyclerView est la solution standard pour afficher des listes performantes. "
        "Il réutilise les vues (recycles) au lieu d'en créer de nouvelles à chaque scroll.", body))
    story.append(code(
"""// Adapter avec DiffUtil pour des mises à jour efficaces
class TaskAdapter(
    private val onTaskClick: (Task) -> Unit,
    private val onCheckChanged: (Task, Boolean) -> Unit
) : ListAdapter<Task, TaskAdapter.TaskViewHolder>(TaskDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TaskViewHolder {
        val binding = ItemTaskBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return TaskViewHolder(binding)
    }

    override fun onBindViewHolder(holder: TaskViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class TaskViewHolder(
        private val binding: ItemTaskBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(task: Task) {
            binding.apply {
                textTitle.text = task.title
                textDescription.text = task.description
                checkboxCompleted.isChecked = task.isCompleted

                // Barrer le texte si la tâche est complétée
                textTitle.paintFlags = if (task.isCompleted)
                    textTitle.paintFlags or Paint.STRIKE_THRU_TEXT_FLAG
                else
                    textTitle.paintFlags and Paint.STRIKE_THRU_TEXT_FLAG.inv()

                // Badge de priorité
                chipPriority.text = task.priority.name
                chipPriority.chipBackgroundColor = ColorStateList.valueOf(
                    when (task.priority) {
                        Priority.HIGH   -> Color.RED
                        Priority.MEDIUM -> Color.parseColor("#FF9800")
                        Priority.LOW    -> Color.parseColor("#4CAF50")
                    }
                )

                root.setOnClickListener { onTaskClick(task) }
                checkboxCompleted.setOnCheckedChangeListener { _, checked ->
                    onCheckChanged(task, checked)
                }
            }
        }
    }
}

// DiffCallback pour des animations fluides
class TaskDiffCallback : DiffUtil.ItemCallback<Task>() {
    override fun areItemsTheSame(old: Task, new: Task) = old.id == new.id
    override fun areContentsTheSame(old: Task, new: Task) = old == new
}"""))

    story.append(Paragraph("2.3 — Responsive Design : Portrait & Paysage", section))
    story.append(Paragraph(
        "Comme tu l'as découvert en pratique, Android charge automatiquement le layout "
        "correspondant à l'orientation depuis les bons dossiers de ressources.", body))

    orient_data = [
        ["Dossier", "Chargé quand"],
        ["res/layout/", "Toujours (fallback)"],
        ["res/layout-land/", "Orientation paysage"],
        ["res/layout-sw600dp/", "Tablettes (≥ 600dp)"],
        ["res/layout-sw600dp-land/", "Tablettes en paysage"],
        ["res/layout-night/", "Mode sombre"],
    ]
    t = Table(orient_data, colWidths=[6*cm, 10*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ANDROID_GREEN),
        ('TEXTCOLOR',  (0,0), (-1,0), TEXT_DARK),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CODE_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCDD')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Paragraph("Tableau 2.1 — Qualificateurs de ressources Android", caption))

    story.append(warn(
        "Quand tu utilises un layout alternatif (land, sw600dp...), assure-toi que "
        "TOUS les IDs référencés dans ton Activity/Fragment existent dans CHAQUE variante du layout. "
        "Un ID manquant provoque un NullPointerException au runtime comme on l'a vu !"))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 3 : JETPACK COMPOSE
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 3", ch_num))
    story.append(Paragraph("Jetpack Compose", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Jetpack Compose est le toolkit UI moderne d'Android. Au lieu de manipuler des vues "
        "XML impérativement, tu décris l'UI en Kotlin avec des fonctions composables. "
        "Le framework se charge de mettre à jour l'écran quand les données changent.", body))

    story.append(Paragraph("3.1 — Composables & Recomposition", section))
    story.append(Paragraph(
        "Un <b>composable</b> est une fonction annotée @Composable qui décrit un élément "
        "d'interface. La <b>recomposition</b> est le mécanisme par lequel Compose "
        "re-exécute les composables dont les données ont changé.", body))
    story.append(code(
"""// Composable de base pour un item de tâche
@Composable
fun TaskItem(
    task: Task,
    onCheckedChange: (Boolean) -> Unit,
    onTaskClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onTaskClick)
            .padding(horizontal = 16.dp, vertical = 4.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Checkbox(
                checked = task.isCompleted,
                onCheckedChange = onCheckedChange
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = task.title,
                    style = MaterialTheme.typography.titleMedium,
                    textDecoration = if (task.isCompleted)
                        TextDecoration.LineThrough else TextDecoration.None
                )
                if (task.description.isNotEmpty()) {
                    Text(
                        text = task.description,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            PriorityChip(priority = task.priority)
        }
    }
}

// Composable pour la liste complète
@Composable
fun TaskList(
    tasks: List<Task>,
    onTaskClick: (Task) -> Unit,
    onCheckChanged: (Task, Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        items(tasks, key = { it.id }) { task ->
            TaskItem(
                task = task,
                onCheckedChange = { checked -> onCheckChanged(task, checked) },
                onTaskClick = { onTaskClick(task) }
            )
        }
    }
}"""))

    story.append(Paragraph("3.2 — State Management avec remember & StateFlow", section))
    story.append(Paragraph(
        "En Compose, l'UI est une <i>fonction de l'état</i>. Quand l'état change, "
        "Compose recompose automatiquement les composables concernés. Il existe plusieurs "
        "façons de gérer l'état selon sa portée.", body))
    story.append(code(
"""// État local avec remember (survit aux recompositions)
@Composable
fun SearchBar(onSearch: (String) -> Unit) {
    var query by remember { mutableStateOf("") }

    OutlinedTextField(
        value = query,
        onValueChange = { newQuery ->
            query = newQuery
            onSearch(newQuery)
        },
        placeholder = { Text("Rechercher une tâche...") },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { query = "" }) {
                    Icon(Icons.Default.Clear, contentDescription = "Effacer")
                }
            }
        },
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    )
}

// État du ViewModel collecté dans un composable
@Composable
fun TaskScreen(viewModel: TaskViewModel = hiltViewModel()) {
    // collectAsStateWithLifecycle respecte le cycle de vie Android
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Error   -> ErrorMessage(state.message)
        is UiState.Success -> TaskList(
            tasks = state.data,
            onTaskClick = viewModel::onTaskClick,
            onCheckChanged = viewModel::onTaskChecked
        )
    }
}"""))

    story.append(Paragraph("3.3 — Thème Material Design 3", section))
    story.append(code(
"""// ui/theme/Theme.kt
private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF7F52FF),          // Violet Kotlin
    onPrimary = Color.White,
    primaryContainer = Color(0xFFEDE7FF),
    secondary = Color(0xFF3DDC84),        // Vert Android
    onSecondary = Color.Black,
    background = Color(0xFFFFFBFE),
    surface = Color(0xFFFFFBFE),
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFFB599FF),
    onPrimary = Color(0xFF2A005F),
    primaryContainer = Color(0xFF3F008F),
    secondary = Color(0xFF3DDC84),
    background = Color(0xFF1C1B1F),
    surface = Color(0xFF1C1B1F),
)

@Composable
fun TaskFlowTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}"""))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 4 : ARCHITECTURE MVVM
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 4", ch_num))
    story.append(Paragraph("Architecture MVVM", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "L'architecture MVVM (Model-View-ViewModel) sépare les responsabilités de l'application "
        "en couches distinctes. C'est le pattern recommandé par Google pour les applications "
        "Android robustes et testables.", body))

    # Schéma d'architecture
    arch_data = [
        ["Couche", "Composants", "Responsabilité"],
        ["UI (View)", "Activity, Fragment, Composable", "Afficher les données, capturer les events"],
        ["ViewModel", "ViewModel, StateFlow", "Logique de présentation, état UI"],
        ["Repository", "Repository, DataSource", "Source unique de vérité pour les données"],
        ["Data", "Room DAO, Retrofit API", "Accès aux données (local + réseau)"],
        ["Model", "Data Class, Entity", "Structure des données"],
    ]
    t = Table(arch_data, colWidths=[3.5*cm, 5.5*cm, 7*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), KOTLIN_PURPLE),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_PURPLE]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCDD')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Paragraph("Tableau 4.1 — Couches de l'architecture MVVM dans TaskFlow", caption))

    story.append(Paragraph("4.1 — ViewModel & StateFlow", section))
    story.append(code(
"""// ViewModel principal de TaskFlow
@HiltViewModel
class TaskViewModel @Inject constructor(
    private val taskRepository: TaskRepository
) : ViewModel() {

    // État UI émis vers l'UI
    private val _uiState = MutableStateFlow<UiState<List<Task>>>(UiState.Loading)
    val uiState: StateFlow<UiState<List<Task>>> = _uiState.asStateFlow()

    // Filtre de recherche
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    // Filtre de statut (toutes / actives / complétées)
    private val _filter = MutableStateFlow(TaskFilter.ALL)
    val filter: StateFlow<TaskFilter> = _filter.asStateFlow()

    // Combine les flows : recalcule quand n'importe lequel change
    val filteredTasks: StateFlow<List<Task>> = combine(
        taskRepository.getAllTasks(),
        _searchQuery,
        _filter
    ) { tasks, query, filter ->
        tasks
            .filter { task ->
                when (filter) {
                    TaskFilter.ALL       -> true
                    TaskFilter.ACTIVE    -> !task.isCompleted
                    TaskFilter.COMPLETED -> task.isCompleted
                }
            }
            .filter { task ->
                query.isEmpty() || task.title.contains(query, ignoreCase = true)
            }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun onSearchQueryChanged(query: String) { _searchQuery.value = query }
    fun onFilterChanged(filter: TaskFilter) { _filter.value = filter }

    fun onTaskChecked(task: Task, isChecked: Boolean) {
        viewModelScope.launch {
            taskRepository.updateTask(task.copy(isCompleted = isChecked))
        }
    }

    fun deleteTask(task: Task) {
        viewModelScope.launch {
            taskRepository.deleteTask(task)
        }
    }
}

enum class TaskFilter { ALL, ACTIVE, COMPLETED }"""))

    story.append(Paragraph("4.2 — Repository Pattern", section))
    story.append(Paragraph(
        "Le Repository est le seul endroit qui décide d'où viennent les données : "
        "du cache local (Room) ou de l'API distante (Retrofit). "
        "L'UI ne sait jamais d'où viennent les données.", body))
    story.append(code(
"""// Interface (contrat)
interface TaskRepository {
    fun getAllTasks(): Flow<List<Task>>
    suspend fun getTaskById(id: Int): Task?
    suspend fun insertTask(task: Task): Long
    suspend fun updateTask(task: Task)
    suspend fun deleteTask(task: Task)
    suspend fun syncWithRemote()
}

// Implémentation
class TaskRepositoryImpl @Inject constructor(
    private val taskDao: TaskDao,          // Source locale (Room)
    private val taskApi: TaskApiService,   // Source distante (Retrofit)
    private val networkChecker: NetworkChecker
) : TaskRepository {

    // Retourne toujours le Flow local (source de vérité)
    override fun getAllTasks(): Flow<List<Task>> = taskDao.getAllTasks()

    override suspend fun syncWithRemote() {
        if (!networkChecker.isConnected()) return
        try {
            val remoteTasks = taskApi.getTasks()
            val localTasks = remoteTasks.map { it.toEntity() }
            taskDao.insertAll(localTasks)  // Upsert
        } catch (e: Exception) {
            // Log l'erreur, les données locales restent disponibles
        }
    }

    override suspend fun insertTask(task: Task): Long {
        val id = taskDao.insert(task)
        // Optionnel : synchro en arrière-plan
        return id
    }

    override suspend fun updateTask(task: Task) = taskDao.update(task)
    override suspend fun deleteTask(task: Task) = taskDao.delete(task)
    override suspend fun getTaskById(id: Int) = taskDao.getById(id)
}"""))

    story.append(Paragraph("4.3 — Injection de dépendances avec Hilt", section))
    story.append(Paragraph(
        "Hilt est la solution d'injection de dépendances recommandée par Google pour Android. "
        "Elle est construite sur Dagger et simplifie considérablement la configuration.", body))
    story.append(code(
"""// 1. Application annotée
@HiltAndroidApp
class TaskFlowApp : Application()

// 2. Module de dépendances
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): TaskDatabase {
        return Room.databaseBuilder(
            context,
            TaskDatabase::class.java,
            "taskflow.db"
        ).build()
    }

    @Provides
    fun provideTaskDao(db: TaskDatabase): TaskDao = db.taskDao()

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl("https://jsonplaceholder.typicode.com/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    @Provides
    fun provideTaskApi(retrofit: Retrofit): TaskApiService =
        retrofit.create(TaskApiService::class.java)
}

// 3. Module Repository
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    @Singleton
    abstract fun bindTaskRepository(
        impl: TaskRepositoryImpl
    ): TaskRepository
}

// 4. Injecter dans Activity / Fragment
@AndroidEntryPoint
class MainActivity : AppCompatActivity() { ... }"""))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 5 : ROOM
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 5", ch_num))
    story.append(Paragraph("Persistance avec Room", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Room est la bibliothèque de persistence Android officielle, construite au-dessus "
        "de SQLite. Elle offre une API type-safe, vérifie les requêtes SQL à la compilation, "
        "et s'intègre parfaitement avec les coroutines et Flow.", body))

    story.append(Paragraph("5.1 — Entité, DAO & Database", section))
    story.append(code(
"""// Entité Room (correspond à une table SQL)
@Entity(tableName = "tasks")
data class TaskEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    @ColumnInfo(name = "title")
    val title: String,
    @ColumnInfo(name = "description")
    val description: String = "",
    @ColumnInfo(name = "is_completed")
    val isCompleted: Boolean = false,
    @ColumnInfo(name = "priority")
    val priority: String = "MEDIUM",
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),
    @ColumnInfo(name = "remote_id")
    val remoteId: Int? = null
)

// Mapper vers/depuis le model domaine
fun TaskEntity.toDomain() = Task(
    id = id, title = title, description = description,
    isCompleted = isCompleted,
    priority = Priority.valueOf(priority),
    createdAt = createdAt
)

fun Task.toEntity() = TaskEntity(
    id = id, title = title, description = description,
    isCompleted = isCompleted, priority = priority.name,
    createdAt = createdAt
)

// DAO (Data Access Object)
@Dao
interface TaskDao {
    @Query("SELECT * FROM tasks ORDER BY created_at DESC")
    fun getAllTasks(): Flow<List<TaskEntity>>  // Flow = observer en temps réel

    @Query("SELECT * FROM tasks WHERE id = :id")
    suspend fun getById(id: Int): TaskEntity?

    @Query("SELECT * FROM tasks WHERE is_completed = :completed")
    fun getByStatus(completed: Boolean): Flow<List<TaskEntity>>

    @Query("SELECT * FROM tasks WHERE title LIKE '%' || :query || '%'")
    fun search(query: String): Flow<List<TaskEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(task: TaskEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(tasks: List<TaskEntity>)

    @Update
    suspend fun update(task: TaskEntity)

    @Delete
    suspend fun delete(task: TaskEntity)

    @Query("DELETE FROM tasks WHERE is_completed = 1")
    suspend fun deleteCompleted()

    @Query("SELECT COUNT(*) FROM tasks WHERE is_completed = 0")
    fun countPending(): Flow<Int>
}

// Database
@Database(
    entities = [TaskEntity::class],
    version = 1,
    exportSchema = false
)
abstract class TaskDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
}"""))

    story.append(Paragraph("5.2 — Migrations", section))
    story.append(Paragraph(
        "Quand tu modifies la structure de ta base de données (ajout d'une colonne, "
        "nouvelle table...), tu dois créer une migration pour éviter de perdre les données "
        "des utilisateurs existants.", body))
    story.append(code(
"""// Migration de la version 1 à 2 (ajout colonne due_date)
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "ALTER TABLE tasks ADD COLUMN due_date INTEGER DEFAULT NULL"
        )
    }
}

// Migration 2 -> 3 (nouvelle table tags)
val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS tags (" +
            "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," +
            "name TEXT NOT NULL," +
            "color TEXT NOT NULL DEFAULT '#7F52FF')"
        )
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS task_tag_cross_ref (" +
            "task_id INTEGER NOT NULL," +
            "tag_id INTEGER NOT NULL," +
            "PRIMARY KEY(task_id, tag_id))"
        )
    }
}

// Enregistrement des migrations dans la Database
@Database(entities = [...], version = 3)
abstract class TaskDatabase : RoomDatabase() {
    companion object {
        fun build(context: Context) = Room.databaseBuilder(
            context, TaskDatabase::class.java, "taskflow.db"
        )
        .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
        .build()
    }
}"""))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 6 : API REST & RÉSEAU
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 6", ch_num))
    story.append(Paragraph("API REST & Réseau avec Retrofit", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Retrofit est la bibliothèque réseau de référence pour Android. "
        "Elle transforme les appels API en fonctions Kotlin suspend, "
        "s'intégrant parfaitement avec les coroutines. "
        "Dans TaskFlow, nous utilisons l'API JSONPlaceholder pour simuler un backend.", body))

    story.append(Paragraph("6.1 — Configuration Retrofit", section))
    story.append(code(
"""// Modèle de réponse API
data class TodoDto(
    val id: Int,
    val userId: Int,
    val title: String,
    val completed: Boolean
)

// Extension pour mapper DTO -> Domain
fun TodoDto.toTask() = Task(
    id = id,
    title = title,
    isCompleted = completed,
    description = "Importé depuis l'API (userId: $userId)"
)

// Interface API avec Retrofit
interface TaskApiService {
    @GET("todos")
    suspend fun getTasks(
        @Query("_limit") limit: Int = 20
    ): List<TodoDto>

    @GET("todos/{id}")
    suspend fun getTask(@Path("id") id: Int): TodoDto

    @POST("todos")
    suspend fun createTask(@Body task: TodoDto): TodoDto

    @PUT("todos/{id}")
    suspend fun updateTask(
        @Path("id") id: Int,
        @Body task: TodoDto
    ): TodoDto

    @DELETE("todos/{id}")
    suspend fun deleteTask(@Path("id") id: Int): Response<Unit>
}

// Configuration avec OkHttp & logging
@Provides
@Singleton
fun provideOkHttpClient(): OkHttpClient {
    return OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = if (BuildConfig.DEBUG)
                HttpLoggingInterceptor.Level.BODY
            else
                HttpLoggingInterceptor.Level.NONE
        })
        .addInterceptor { chain ->
            // Intercepteur d'authentification
            val request = chain.request().newBuilder()
                .addHeader("Authorization", "Bearer \${BuildConfig.API_TOKEN}")
                .addHeader("Accept", "application/json")
                .build()
            chain.proceed(request)
        }
        .build()
}"""))

    story.append(Paragraph("6.2 — Gestion d'erreurs avec sealed class Result", section))
    story.append(Paragraph(
        "Une API peut échouer pour de nombreuses raisons : pas de réseau, timeout, "
        "erreur serveur 500, réponse malformée... Il faut gérer tous ces cas "
        "élégamment sans faire planter l'application.", body))
    story.append(code(
"""// Wrapper Result générique
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(
        val exception: Exception,
        val message: String = exception.message ?: "Erreur inconnue"
    ) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// Extension pour simplifier les appels Retrofit
suspend fun <T> safeApiCall(apiCall: suspend () -> T): Result<T> {
    return try {
        Result.Success(apiCall())
    } catch (e: HttpException) {
        val message = when (e.code()) {
            401 -> "Non autorisé - vérifiez votre connexion"
            403 -> "Accès interdit"
            404 -> "Ressource introuvable"
            500 -> "Erreur serveur, réessayez plus tard"
            else -> "Erreur réseau : \${e.code()}"
        }
        Result.Error(e, message)
    } catch (e: IOException) {
        Result.Error(e, "Pas de connexion internet")
    } catch (e: Exception) {
        Result.Error(e, "Erreur inattendue : \${e.message}")
    }
}

// Utilisation dans le Repository
class TaskRepositoryImpl @Inject constructor(
    private val taskApi: TaskApiService,
    private val taskDao: TaskDao
) : TaskRepository {

    override suspend fun syncWithRemote(): Result<Unit> {
        return when (val result = safeApiCall { taskApi.getTasks() }) {
            is Result.Success -> {
                val entities = result.data.map { it.toTask().toEntity() }
                taskDao.insertAll(entities)
                Result.Success(Unit)
            }
            is Result.Error -> result
            Result.Loading -> Result.Loading
        }
    }
}

// Dans le ViewModel
fun syncTasks() {
    viewModelScope.launch {
        _uiState.value = UiState.Loading
        when (val result = taskRepository.syncWithRemote()) {
            is Result.Success -> _uiState.value = UiState.Success(Unit)
            is Result.Error   -> _uiState.value = UiState.Error(result.message)
            Result.Loading    -> { /* déjà géré */ }
        }
    }
}"""))

    story.append(tip("Utilise un intercepteur OkHttp pour logger toutes tes requêtes en mode "
                     "DEBUG. En production, désactive le logging pour ne pas exposer les tokens "
                     "et données sensibles dans les logs."))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 7 : NAVIGATION
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 7", ch_num))
    story.append(Paragraph("Navigation & Deep Links", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Le Jetpack Navigation Component gère la navigation entre les écrans, "
        "le back stack, les animations et les deep links de manière centralisée. "
        "Avec Compose, on utilise la Navigation Compose.", body))

    story.append(Paragraph("7.1 — Navigation Compose", section))
    story.append(code(
"""// Définition des routes de navigation
sealed class Screen(val route: String) {
    object TaskList   : Screen("tasks")
    object TaskDetail : Screen("tasks/{taskId}") {
        fun createRoute(taskId: Int) = "tasks/$taskId"
    }
    object AddTask    : Screen("tasks/add")
    object Settings   : Screen("settings")
}

// NavHost principal
@Composable
fun TaskFlowNavHost(
    navController: NavHostController = rememberNavController(),
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Screen.TaskList.route,
        modifier = modifier
    ) {
        composable(Screen.TaskList.route) {
            TaskListScreen(
                onTaskClick = { task ->
                    navController.navigate(Screen.TaskDetail.createRoute(task.id))
                },
                onAddClick = {
                    navController.navigate(Screen.AddTask.route)
                }
            )
        }

        composable(
            route = Screen.TaskDetail.route,
            arguments = listOf(navArgument("taskId") { type = NavType.IntType })
        ) { backStackEntry ->
            val taskId = backStackEntry.arguments?.getInt("taskId") ?: return@composable
            TaskDetailScreen(
                taskId = taskId,
                onBack = { navController.popBackStack() },
                onDelete = {
                    navController.popBackStack()
                }
            )
        }

        composable(
            route = Screen.AddTask.route,
            enterTransition = {
                slideInVertically(initialOffsetY = { it })
            },
            exitTransition = {
                slideOutVertically(targetOffsetY = { it })
            }
        ) {
            AddTaskScreen(
                onTaskSaved = { navController.popBackStack() },
                onCancel = { navController.popBackStack() }
            )
        }
    }
}

// Bottom Navigation Bar
@Composable
fun TaskFlowBottomBar(navController: NavController) {
    val items = listOf(
        Screen.TaskList to Icons.Default.List,
        Screen.Settings to Icons.Default.Settings
    )
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    NavigationBar {
        items.forEach { (screen, icon) ->
            NavigationBarItem(
                icon = { Icon(icon, contentDescription = null) },
                label = { Text(screen.route) },
                selected = currentRoute == screen.route,
                onClick = {
                    navController.navigate(screen.route) {
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}"""))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CHAPITRE 8 : PROJET TASKFLOW COMPLET
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPITRE 8", ch_num))
    story.append(Paragraph("Projet TaskFlow — Assemblage Final", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Ce chapitre assemble toutes les pièces du projet TaskFlow. "
        "Voici la structure complète du projet et les fichiers clés qui font "
        "fonctionner l'application bout en bout.", body))

    story.append(Paragraph("8.1 — Structure du projet", section))
    story.append(code(
"""app/
├── build.gradle.kts
└── src/main/
    ├── AndroidManifest.xml
    └── java/com/example/taskflow/
        ├── TaskFlowApp.kt              // @HiltAndroidApp
        ├── data/
        │   ├── local/
        │   │   ├── TaskDatabase.kt     // Room Database
        │   │   ├── TaskDao.kt          // DAO
        │   │   └── TaskEntity.kt       // Entity Room
        │   ├── remote/
        │   │   ├── TaskApiService.kt   // Interface Retrofit
        │   │   └── TodoDto.kt          // Data Transfer Object
        │   └── repository/
        │       ├── TaskRepository.kt   // Interface
        │       └── TaskRepositoryImpl.kt
        ├── domain/
        │   ├── model/
        │   │   └── Task.kt             // Modèle domaine
        │   └── util/
        │       ├── Result.kt           // Sealed class
        │       └── UiState.kt
        ├── di/
        │   ├── AppModule.kt            // Module Hilt
        │   └── RepositoryModule.kt
        ├── ui/
        │   ├── MainActivity.kt
        │   ├── navigation/
        │   │   └── TaskFlowNavHost.kt
        │   ├── tasklist/
        │   │   ├── TaskListScreen.kt   // Composable
        │   │   └── TaskViewModel.kt
        │   ├── taskdetail/
        │   │   ├── TaskDetailScreen.kt
        │   │   └── TaskDetailViewModel.kt
        │   ├── addtask/
        │   │   ├── AddTaskScreen.kt
        │   │   └── AddTaskViewModel.kt
        │   └── theme/
        │       ├── Theme.kt
        │       ├── Color.kt
        │       └── Type.kt
        └── util/
            └── Extensions.kt"""))

    story.append(Paragraph("8.2 — build.gradle.kts complet", section))
    story.append(code(
"""plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.hilt.android)
    alias(libs.plugins.ksp)
}

android {
    namespace = "com.example.taskflow"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.taskflow"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    // Compose BOM (gère toutes les versions Compose)
    val composeBom = platform(libs.androidx.compose.bom)
    implementation(composeBom)
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.material3)
    implementation(libs.androidx.activity.compose)

    // ViewModel + Lifecycle
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)

    // Navigation Compose
    implementation(libs.androidx.navigation.compose)

    // Hilt (DI)
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.androidx.hilt.navigation.compose)

    // Room
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)

    // Retrofit + OkHttp
    implementation(libs.retrofit)
    implementation(libs.converter.gson)
    implementation(libs.okhttp)
    implementation(libs.logging.interceptor)

    // Coroutines
    implementation(libs.kotlinx.coroutines.android)

    // Tests
    testImplementation(libs.junit)
    testImplementation(libs.kotlinx.coroutines.test)
    testImplementation(libs.mockk)
    androidTestImplementation(libs.androidx.espresso.core)
}"""))

    story.append(Paragraph("8.3 — MainActivity & Point d'entrée Compose", section))
    story.append(code(
"""@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            TaskFlowTheme {
                val navController = rememberNavController()
                Scaffold(
                    bottomBar = {
                        TaskFlowBottomBar(navController = navController)
                    }
                ) { innerPadding ->
                    TaskFlowNavHost(
                        navController = navController,
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}"""))

    story.append(Paragraph("8.4 — Tests Unitaires du ViewModel", section))
    story.append(code(
"""class TaskViewModelTest {

    // Règle pour remplacer le Main dispatcher par un TestDispatcher
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val taskRepository: TaskRepository = mockk()
    private lateinit var viewModel: TaskViewModel

    @Before
    fun setup() {
        // Stub du repository
        coEvery { taskRepository.getAllTasks() } returns flowOf(
            listOf(
                Task(id = 1, title = "Tâche 1", isCompleted = false),
                Task(id = 2, title = "Tâche 2", isCompleted = true)
            )
        )
        viewModel = TaskViewModel(taskRepository)
    }

    @Test
    fun `filteredTasks retourne toutes les tâches par défaut`() = runTest {
        val tasks = viewModel.filteredTasks.first()
        assertEquals(2, tasks.size)
    }

    @Test
    fun `filtre ACTIVE retourne seulement les tâches non complétées`() = runTest {
        viewModel.onFilterChanged(TaskFilter.ACTIVE)
        val tasks = viewModel.filteredTasks.first()
        assertEquals(1, tasks.size)
        assertFalse(tasks.first().isCompleted)
    }

    @Test
    fun `recherche filtre par titre`() = runTest {
        viewModel.onSearchQueryChanged("Tâche 1")
        val tasks = viewModel.filteredTasks.first()
        assertEquals(1, tasks.size)
        assertEquals("Tâche 1", tasks.first().title)
    }

    @Test
    fun `onTaskChecked met à jour la tâche`() = runTest {
        val task = Task(id = 1, title = "Test")
        coEvery { taskRepository.updateTask(any()) } just Runs
        viewModel.onTaskChecked(task, true)
        coVerify { taskRepository.updateTask(task.copy(isCompleted = true)) }
    }
}

// Règle utilitaire pour les tests
class MainDispatcherRule(
    val testDispatcher: TestCoroutineDispatcher = TestCoroutineDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }
    override fun finished(description: Description) {
        Dispatchers.resetMain()
        testDispatcher.cleanupTestCoroutines()
    }
}"""))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════
    # CONCLUSION
    # ════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CONCLUSION", ch_num))
    story.append(Paragraph("Prochaines Étapes & Ressources", ch_title))
    story.append(HR())
    story.append(Paragraph(
        "Félicitations ! Tu maîtrises maintenant les fondamentaux du développement Android moderne "
        "avec Kotlin. Le projet TaskFlow t'a permis de mettre en pratique l'architecture MVVM, "
        "Room, Retrofit, Compose et la navigation. Voici la suite logique de ton apprentissage.", body))

    story.append(Paragraph("Sujets avancés à explorer", section))

    next_topics = [
        ("WorkManager", "Tâches de fond planifiées (synchro périodique, upload de fichiers)"),
        ("DataStore", "Remplacement moderne de SharedPreferences (clé-valeur ou Proto)"),
        ("Paging 3", "Chargement de listes infinies paginées depuis une API"),
        ("CameraX", "Intégration de la caméra avec prévisualisation et capture"),
        ("Notifications", "Notifications push avec Firebase Cloud Messaging (FCM)"),
        ("Tests E2E", "Tests d'interface avec Espresso ou UI Automator"),
        ("CI/CD", "Automatisation des builds et déploiements avec GitHub Actions"),
        ("Play Store", "Signature, optimisation APK/AAB, release et mises à jour"),
    ]

    for title_t, desc in next_topics:
        story.append(KeepTogether([
            Paragraph(f"◆ {title_t}", S('NextTitle', fontName='Helvetica-Bold',
                fontSize=12, textColor=KOTLIN_PURPLE, spaceBefore=10, spaceAfter=2)),
            Paragraph(desc, S('NextDesc', fontName='Helvetica', fontSize=10,
                textColor=GREY_TEXT, leftIndent=16, spaceAfter=4))
        ]))

    story.append(Paragraph("Ressources officielles", section))
    res_data = [
        ["Ressource", "URL"],
        ["Documentation Android", "developer.android.com"],
        ["Jetpack Compose", "developer.android.com/compose"],
        ["Kotlin", "kotlinlang.org"],
        ["Codelabs Google", "codelabs.developers.google.com"],
        ["Android Developers YouTube", "youtube.com/@AndroidDevelopers"],
        ["Now in Android (app exemple)", "github.com/android/nowinandroid"],
    ]
    t = Table(res_data, colWidths=[6*cm, 10*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), KOTLIN_PURPLE),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_PURPLE]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCDD')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)

    story.append(Spacer(1, 1*cm))
    story.append(HR(ANDROID_GREEN, 2))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "\"The best way to learn Android development is to build apps. "
        "Build something you care about, break it, fix it, and build it better.\"",
        S('Quote', fontName='Helvetica-Oblique', fontSize=13,
          textColor=KOTLIN_PURPLE, alignment=TA_CENTER, spaceBefore=10)))
    story.append(Paragraph(
        "Bonne continuation dans ton parcours de développeur Android ! 🚀",
        S('Closing', fontName='Helvetica-Bold', fontSize=14,
          textColor=TEXT_DARK, alignment=TA_CENTER, spaceBefore=12)))

    return story


# ── Construction du PDF ──────────────────────────────────────────────────
def main():
    output_path = "/mnt/user-data/outputs/Developpement_Android_Kotlin.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        title="Développement Android avec Kotlin",
        author="Guide Pratique Complet",
        subject="Android, Kotlin, Jetpack Compose, MVVM, Room, Retrofit",
    )

    story = build_story()

    # Page de couverture sans en-tête/pied de page
    def on_first_page(canvas, doc):
        CoverPage().build(canvas, doc)

    def on_later_pages(canvas, doc):
        on_page(canvas, doc)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF généré : {output_path}")

if __name__ == "__main__":
    main()
