const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const http = require('http');

// --- CONFIGURATION ---
const DOSSIER_RACINE = "/media/edithson/Ventoy/DOSSIERS ADMIN 2/PUBLIC";
const NOM_DOSSIER_SUCCES = 'Fichiers_Archives_Succes';
const URL_ARCHIVES = 'http://172.20.9.254:8000/archives';
const old_login = 'cyril.fonyuy';
const old_password = 'OOOOOOOO';
const user_login = 'archive@mail.com';
const password = 'OOOOO';

// Variable pour définir le séparateur du nom de fichier (' ' ou '_') et le service cible
const SEPARATEUR_NOM_FICHIER = ' '; 
const SERVICE_CIBLE = 'PUBLIC'; // Accepte le sigle ('SO', 'DCOB'...) ou le nom complet

// --- DICTIONNAIRE DES DÉPARTEMENTS (Sigle value -> Libellé complet) ---
const DICTIONNAIRE_DEPARTEMENTS = {
    'CAB DGB': "CABINET DGB (CAB DGB)",
    'DDPP': "DIRECTION DE LA DEPENSE DE PERSONNEL ET DES PENSIONS (DDPP)",
    'DI': "DIVISION INFORMATIQUE (DI)",
    'DPB': "DIVISION DE LA PREPARATION DU BUDGET (DPB)",
    'DREF': "DIVISION DE LA REFORME BUDGETAIRE (DREF)",
    'DPC': "DIVISION DES PARTICIPATIONS ET DES CONTRIBUTIONS (DPC)",
    'DCOB': "DIVISION DU CONTROLE BUDGETAIRE DE L'AUDIT ET DE LA QUALITE DE LA DEPENSE (DCOB)",
    'SO': "SERVICE D'ORDRE (SO)",
    'SGDB': "SERVICE DE GESTION DES DOCUMENTS BUDGETAIRES (SGDB)",
    'SGCCC': "SERVICE DE GESTION DES CREDITS DES CHAPITRES COMMUNS (SGCCC)",
    'S-DAG': "SOUS DIRECTION DES AFFAIRES GENERALES (S-DAG)",
    'S-DCF': "SOUS DIRECTION DU CONTROLE FINANCIER (S-DCF)",
    'PUBLIC': "PUBLIC (PUBLIC)"
};

function resoudreDepartement(cible) {
    const cle = cible.trim().toUpperCase();
    if (DICTIONNAIRE_DEPARTEMENTS[cle]) {
        return { value: cle, label: DICTIONNAIRE_DEPARTEMENTS[cle] };
    }
    for (const [code, libelle] of Object.entries(DICTIONNAIRE_DEPARTEMENTS)) {
        if (libelle.toUpperCase() === cle) {
            return { value: code, label: libelle };
        }
    }
    console.warn(`⚠️ Département "${cible}" non répertorié dans DICTIONNAIRE_DEPARTEMENTS, utilisation directe de la valeur.`);
    return { value: cible.trim(), label: cible.trim() };
}

const DEPARTEMENT_CIBLE = resoudreDepartement(SERVICE_CIBLE);

// --- DICTIONNAIRE INTELLIGENT (Prioritaire sur le 1er mot du fichier) ---
const DICTIONNAIRE_NATURES = {
    'DECI': 'DECISIONS', 'FD': 'FONDS DE DOSSIER', 'ESD': 'ETATS DE SOMMES DUES', 'NOTE': 'NOTE DE SERVICE',
    'COMMUNIQUE': 'COMMUNIQUES', 'CONVOCATION': 'CONVOCATIONS', 'COURA': 'COURRIERS',
    'ST': 'SOIT-TRANSMIS', 'SOIT': 'SOIT-TRANSMIS', 'INVITATION': 'INVITATIONS',
    'COURRIERS': 'COURRIERS', 'MARCHE': 'MARCHE',
    'INSTRUCTIONS': 'INSTRUCTIONS', 'CONSTITUTION': 'CONSTITUTION', 'LOI': 'LOI',
    'LETTRE-DE-MISSION': 'LETTRE DE MISSION', 'ARRETE': 'ARRETE', 'DECRET': 'DECRET',
    'DOSSIER-DU-PERSONNEL': 'DOSSIER DU PERSONNEL', 'DOSSIER-DES-PENSIONS': 'DOSSIER DES PENSIONS',
    'RAPPORTS': 'RAPPORTS', 'DECISIONS': 'DECISIONS', 'FONDS-DE-DOSSIER': 'FONDS DE DOSSIER',
    'LETTRE': 'LETTRE DE MISSION', 'RAPPORT': 'RAPPORTS', 'FICHE': 'DOSSIER DU PERSONNEL',
    'CERTIF': 'DOSSIER DU PERSONNEL', 'BE': 'BONS D\'ENGAGEMENT', 'COMPTE': 'COMPTE RENDU',
    'DECISION': 'DECISIONS', 'DEMANDE': 'DEMANDES', 'MEMO': 'MEMO',
    'ACCOMPAGNEMENT': 'AUTRES TYPES DE DOCUMENTS', 'ACCORD': 'AUTRES TYPES DE DOCUMENTS',
    'ACCREDITATION': 'AUTRES TYPES DE DOCUMENTS', 'ACHAT': 'AUTRES TYPES DE DOCUMENTS',
    'ALLEGATIONS': 'AUTRES TYPES DE DOCUMENTS', 'AMBASSADE': 'AUTRES TYPES DE DOCUMENTS',
    'ANNEXES': 'AUTRES TYPES DE DOCUMENTS',
    'APPENDIX': 'AUTRES TYPES DE DOCUMENTS', 'APPLICATION': 'AUTRES TYPES DE DOCUMENTS',
    'APPUI': 'AUTRES TYPES DE DOCUMENTS', 'ATTRIBUTION': 'AUTRES TYPES DE DOCUMENTS',
    'AUTORISATION': 'AUTRES TYPES DE DOCUMENTS', 'BORDEREAU': 'BORDEREAUX', 
    'BUDGET': 'AUTRES TYPES DE DOCUMENTS', 'BUDGETISATION': 'AUTRES TYPES DE DOCUMENTS',
    'CAHIER': 'AUTRES TYPES DE DOCUMENTS', 'CAPTURE': 'AUTRES TYPES DE DOCUMENTS',
    'CERTIFICAT': 'CERTIFICATS', 'CIRCULAIRE': 'AUTRES TYPES DE DOCUMENTS',
    'CIRCULAR': 'AUTRES TYPES DE DOCUMENTS', 'CLOTURE': 'AUTRES TYPES DE DOCUMENTS',
    'CONFRERENCE': 'AUTRES TYPES DE DOCUMENTS', 'CONTINUITE': 'AUTRES TYPES DE DOCUMENTS',
    'COORDINATION': 'AUTRES TYPES DE DOCUMENTS', 'CREATION': 'AUTRES TYPES DE DOCUMENTS',
    'DATE': 'AUTRES TYPES DE DOCUMENTS', 'DEMANE': 'DEMANDES',
    'DENONCIATION': 'AUTRES TYPES DE DOCUMENTS', 'DEPLOIEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'DEPOTS': 'AUTRES TYPES DE DOCUMENTS', 'DEROGATION': 'AUTRES TYPES DE DOCUMENTS',
    'DESIGNATION': 'AUTRES TYPES DE DOCUMENTS', 'DIALOGUE': 'AUTRES TYPES DE DOCUMENTS',
    'DOCUMENTS': 'AUTRES TYPES DE DOCUMENTS', 'EDITION': 'AUTRES TYPES DE DOCUMENTS',
    'ENTREVUE': 'AUTRES TYPES DE DOCUMENTS', 'ETAT': 'AUTRES TYPES DE DOCUMENTS',
    'EXECUTION': 'AUTRES TYPES DE DOCUMENTS', 'EXTENSION': 'AUTRES TYPES DE DOCUMENTS',
    'FINANCEMENT': 'AUTRES TYPES DE DOCUMENTS', 'FODECC': 'AUTRES TYPES DE DOCUMENTS',
    'FONCTIONNEMENT': 'AUTRES TYPES DE DOCUMENTS', 'FORMATION': 'AUTRES TYPES DE DOCUMENTS',
    'IMPREGNATION': 'AUTRES TYPES DE DOCUMENTS', 'INFORMATION': 'AUTRES TYPES DE DOCUMENTS',
    'INSTRUCTION': 'INSTRUCTIONS', 'INVENTAIRE': 'AUTRES TYPES DE DOCUMENTS',
    'INVITATAION': 'INVITATIONS', 'LANCEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'LAW': 'LOI', 'LIVRAISON': 'AUTRES TYPES DE DOCUMENTS',
    'MAIL': 'AUTRES TYPES DE DOCUMENTS', 'MESURES': 'AUTRES TYPES DE DOCUMENTS',
    'MINUTES': 'AUTRES TYPES DE DOCUMENTS', 'MISE': 'AUTRES TYPES DE DOCUMENTS',
    'MISSION': 'LETTRE DE MISSION', 'NASLA': 'AUTRES TYPES DE DOCUMENTS',
    'NON': 'AUTRES TYPES DE DOCUMENTS', 'NOTIFICATION': 'AUTRES TYPES DE DOCUMENTS',
    'OBSERVATION': 'AUTRES TYPES DE DOCUMENTS', 'OUVERTURE': 'AUTRES TYPES DE DOCUMENTS',
    'PAIEMENT': 'AUTRES TYPES DE DOCUMENTS', 'PRIOR': 'AUTRES TYPES DE DOCUMENTS',
    'PROBLEMATIQUE': 'AUTRES TYPES DE DOCUMENTS', 'PROCURATION': 'AUTRES TYPES DE DOCUMENTS',
    'PRODUCTION': 'AUTRES TYPES DE DOCUMENTS', 'PROJET': 'AUTRES TYPES DE DOCUMENTS',
    'PROROGATION': 'AUTRES TYPES DE DOCUMENTS', 'PROTOCOLE': 'AUTRES TYPES DE DOCUMENTS',
    'PV': 'PROCES-VERBAL', 'RAPORT': 'RAPPORTS', 'RAPPEL': 'AUTRES TYPES DE DOCUMENTS',
    'RECLAMATION': 'AUTRES TYPES DE DOCUMENTS', 'RECLASSEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'RECOUVREMENT': 'AUTRES TYPES DE DOCUMENTS', 'RELANCE': 'AUTRES TYPES DE DOCUMENTS',
    'REMUNERATION': 'AUTRES TYPES DE DOCUMENTS', 'REPONSE': 'AUTRES TYPES DE DOCUMENTS',
    'REPONSES': 'AUTRES TYPES DE DOCUMENTS', 'REPORT': 'AUTRES TYPES DE DOCUMENTS',
    'REPRISE': 'AUTRES TYPES DE DOCUMENTS', 'REQUETE': 'AUTRES TYPES DE DOCUMENTS',
    'RETABLISSEMENT': 'AUTRES TYPES DE DOCUMENTS', 'RETRAIT': 'AUTRES TYPES DE DOCUMENTS',
    'REUNION': 'AUTRES TYPES DE DOCUMENTS', 'REVERSEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'SEMINAIRE': 'AUTRES TYPES DE DOCUMENTS', 'SITUATION': 'AUTRES TYPES DE DOCUMENTS',
    'STAGE': 'AUTRES TYPES DE DOCUMENTS', 'SYNTHESE': 'AUTRES TYPES DE DOCUMENTS',
    'TERMES': 'AUTRES TYPES DE DOCUMENTS', 'TRAITEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'TRANSMISSION': 'AUTRES TYPES DE DOCUMENTS', 'TRAVAUX': 'AUTRES TYPES DE DOCUMENTS',
    'VISA': 'AUTRES TYPES DE DOCUMENTS', 'BORDEREAUX': 'BORDEREAUX', 'CESSATION': 'BORDEREAUX',
    'ANNAXE': 'RAPPORTS', 'ANNAXES': 'RAPPORTS', 'ANNEXE': 'RAPPORTS', 'ANNEX': 'RAPPORTS',
    'ATTESTATIONS': 'ATTESTATION', 'ATTESTATION': 'ATTESTATION', 'MESSAGE': 'MESSAGE-FAX'
};

let totalFichiersReussis = 0;
let listeGlobaleEchecs = [];

// ==========================================
// 1. MODULE DE VALIDATION ET D'EXTRACTION
// ==========================================
function validerEtExtraireInfos(nomFichier) {
    const nomSansExt = nomFichier.replace(/\.pdf$/i, '').trim();
    const parts = nomSansExt.split(SEPARATEUR_NOM_FICHIER).map(p => p.trim()).filter(Boolean);

    if (parts.length < 3) {
        throw new Error(`STRUCTURE_INVALIDE: Manque d'informations (séparateur '${SEPARATEUR_NOM_FICHIER}').`);
    }

    const prefixBrut = parts[0].toUpperCase();
    const traductionDico = DICTIONNAIRE_NATURES[prefixBrut];

    // Ordre de priorité : 1. Dictionnaire (si défini) -> 2. 1er élément exact du fichier
    const candidatsNature = [];
    if (traductionDico) {
        candidatsNature.push(traductionDico);
    }
    if (!candidatsNature.includes(prefixBrut)) {
        candidatsNature.push(prefixBrut);
    }

    const dateStr = parts[parts.length - 1];
    if (!/^\d{8}$/.test(dateStr)) {
        throw new Error(`STRUCTURE_INVALIDE: La fin du fichier ('${dateStr}') n'est pas une date à 8 chiffres.`);
    }

    const jour = dateStr.substring(0, 2);
    const mois = dateStr.substring(2, 4);
    const annee = dateStr.substring(4, 8);

    const jourNum = Number(jour);
    const moisNum = Number(mois);
    if (jourNum < 1 || jourNum > 31 || moisNum < 1 || moisNum > 12) {
        throw new Error(`STRUCTURE_INVALIDE: Date incohérente ('${dateStr}').`);
    }

    return {
        candidatsNature,
        nomSansExt,
        dateFormatee: `${annee}-${mois}-${jour}`
    };
}

// ==========================================
// 2. LE SONAR RÉSEAU
// ==========================================
function pingServeur() {
    return new Promise((resolve) => {
        const req = http.get('http://172.20.9.254:8000', (res) => {
            resolve(true);
            res.resume();
        }).on('error', () => resolve(false));

        req.setTimeout(3000, () => {
            req.destroy();
            resolve(false);
        });
    });
}

async function ecouterReseauEtMettreEnPause() {
    let estEnLigne = await pingServeur();
    if (!estEnLigne) {
        console.log("\n      📡 [ALERTE] Connexion perdue avec le serveur (172.20.9.254) !");
        console.log("      ⏳ L'automate active la STASE. Il reprendra dès le retour du réseau...");

        while (!estEnLigne) {
            await new Promise(r => setTimeout(r, 5000));
            estEnLigne = await pingServeur();
        }
        console.log("      ✅ [RÉSEAU RÉTABLI] Connexion retrouvée ! Fin de la stase.\n");
    }
}

// ==========================================
// 3. UTILITAIRES D'INTERFACE & UPLOAD
// ==========================================
function echapperRegex(texte) {
    return texte.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

async function selectionnerTypeArchive(page, candidats) {
    const champType = page.locator('#typearchive');
    const conteneurType = page.locator('div.relative:has(#typearchive)');

    for (const candidat of candidats) {
        await champType.click();
        await champType.fill('');
        await champType.fill(candidat);

        // Recherche uniquement le bouton dont le texte complet est strictement identique au candidat
        const regexExacte = new RegExp(`^\\s*${echapperRegex(candidat)}\\s*$`, 'i');
        const optionExacte = conteneurType.locator('ul button').filter({ hasText: regexExacte });

        try {
            await optionExacte.first().waitFor({ state: 'visible', timeout: 3000 });
            await optionExacte.first().click();
            console.log(`      -> 🏷️ Type d'archive retenu : "${candidat}"`);
            return;
        } catch (_) {
            // Aucune correspondance exacte pour ce candidat, passage au suivant
        }
    }

    throw new Error(`TYPE_INTROUVABLE: Aucune option exacte dans le menu pour [${candidats.join(' -> ')}].`);
}

async function reinitialiserFormulaire(page) {
    try {
        const lienNouvelleArchive = page.locator('a:has-text("Nouvelle Archive")');
        if (await lienNouvelleArchive.count() > 0) {
            await lienNouvelleArchive.click();
            await page.waitForSelector('input[type="file"]', { state: 'attached', timeout: 15000 });
            return;
        }
    } catch (_) {
        // Repli vers un rechargement complet si la réinitialisation douce échoue
    }
    await page.goto(URL_ARCHIVES, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
}

async function traiterFichier(page, cheminComplet, infosFichier) {
    // ÉTAPE 1 : Upload
    await page.waitForSelector('input[type="file"]', { state: 'attached', timeout: 90000 });
    await page.locator('input[type="file"]').setInputFiles(cheminComplet);

    const btnSuivant = page.locator('button:has-text("Étape suivante : Métadonnées")');
    await btnSuivant.waitFor({ state: 'visible', timeout: 30000 });
    await btnSuivant.click();

    // ÉTAPE 2 : Métadonnées
    await page.waitForSelector('select[name="format"]', { state: 'attached', timeout: 90000 });
    await page.locator('select[name="format"]').selectOption('Document PDF', { force: true });
    
    // Sélection stricte avec priorité Dictionnaire -> 1er mot du fichier
    await selectionnerTypeArchive(page, infosFichier.candidatsNature);

    await page.locator('#description').fill(infosFichier.nomSansExt);
    await page.locator('#date_doc').fill(infosFichier.dateFormatee);
    
    // Remplissage conditionnel (Anti-Crash pour comptes restreints)
    if (await page.locator('select:has(option[value="DGB"])').count() > 0) {
        await page.locator('select:has(option[value="DGB"])').selectOption('DGB', { force: true });
    }
    
    if (await page.locator('select:has(option[value="Serveur"])').count() > 0) {
        await page.locator('select:has(option[value="Serveur"])').selectOption('Serveur', { force: true });
    }
    
    if (await page.locator('#rayon').count() > 0) {
        await page.locator('#rayon').fill('B6');
    }
    
    if (await page.locator('#cote').count() > 0) {
        await page.locator('#cote').fill('C1560-40DE.10');
    }
    
    // Sélection du département (value court + repli visuel sur le libellé détaillé)
    const selectDept = page.locator(`select:has(option[value="${DEPARTEMENT_CIBLE.value}"])`);
    const boutonDept = page.locator('#departement');

    if (await selectDept.count() > 0) {
        await selectDept.selectOption({ value: DEPARTEMENT_CIBLE.value }, { force: true });

        if (await boutonDept.count() > 0 && (await boutonDept.getAttribute('data-placeholder')) !== null) {
            await boutonDept.click();
            const optionVisuelle = page.getByRole('option', { name: DEPARTEMENT_CIBLE.label, exact: true });
            await optionVisuelle.waitFor({ state: 'visible', timeout: 5000 });
            await optionVisuelle.click();
        }
    } else if (await boutonDept.count() > 0) {
        console.warn(`      ⚠️ Le département "${DEPARTEMENT_CIBLE.value}" n'est pas disponible pour ce compte utilisateur.`);
    }

    // VALIDATION
    const boutonValider = page.locator('button:has-text("Valider & Créer l\'archive")');
    await boutonValider.waitFor({ state: 'visible', timeout: 90000 });
    
    console.log("      -> Étape 2 : Validation... (Attente réponse serveur : max 180s)");

    const reponseServeurPromise = page.waitForResponse(
        response => response.request().method() !== 'GET' && response.status() >= 200 && response.status() < 400,
        { timeout: 180000 }
    );

    await boutonValider.click();
    await reponseServeurPromise;
    console.log("      -> ✅ Upload confirmé par le serveur !");
    
    // RÉINITIALISATION
    await page.waitForTimeout(1000); 
    console.log("      -> 🔄 Réinitialisation du formulaire via le menu latéral...");
    await reinitialiserFormulaire(page);
}

// ==========================================
// 4. L'EXPLORATEUR RÉCURSIF
// ==========================================
async function parcourirEtTraiterDossier(dossierActuel, page) {
    console.log(`\n📂 [EXPLORATION] Analyse : ${dossierActuel}`);

    const elements = fs.readdirSync(dossierActuel, { withFileTypes: true });
    const fichiersPDF = [];
    const sousDossiers = [];

    for (const el of elements) {
        if (el.isDirectory()) {
            if (el.name !== NOM_DOSSIER_SUCCES) sousDossiers.push(el.name);
        } else if (el.isFile() && el.name.toLowerCase().endsWith('.pdf')) {
            fichiersPDF.push(el.name);
        }
    }

    if (fichiersPDF.length > 0) {
        console.log(`   📄 ${fichiersPDF.length} fichier(s) PDF trouvé(s).`);
        let echecsLocaux = [];

        for (const nomFichier of fichiersPDF) {
            const cheminComplet = path.join(dossierActuel, nomFichier);
            try {
                console.log(`\n   [1/2] Analyse : ${nomFichier}`);
                const infosExtraites = validerEtExtraireInfos(nomFichier);
                await ecouterReseauEtMettreEnPause();
                
                await traiterFichier(page, cheminComplet, infosExtraites);
                
                const cheminDossierSucces = path.join(dossierActuel, NOM_DOSSIER_SUCCES);
                if (!fs.existsSync(cheminDossierSucces)) fs.mkdirSync(cheminDossierSucces);
                fs.renameSync(cheminComplet, path.join(cheminDossierSucces, nomFichier));
                
                totalFichiersReussis++;

            } catch (e) {
                if (e.message.startsWith('STRUCTURE_INVALIDE')) {
                    console.error(`      ❌ Rejeté (Format Invalide) : ${e.message.replace('STRUCTURE_INVALIDE: ', '')}`);
                    listeGlobaleEchecs.push(`[FORMAT INVALIDE] ${cheminComplet}`);
                } else if (e.message.startsWith('TYPE_INTROUVABLE')) {
                    console.error(`      ❌ Upload annulé : ${e.message.replace('TYPE_INTROUVABLE: ', '')}`);
                    listeGlobaleEchecs.push(`[TYPE INTROUVABLE] ${cheminComplet}`);
                    console.log("      -> 🔄 Purge du fichier en cours et retour à l'étape 1...");
                    await reinitialiserFormulaire(page);
                } else {
                    console.error(`      ⚠️ Échec (Timeout/Réseau) : ${e.message.split('\n')[0]}`);
                    echecsLocaux.push(nomFichier);
                    await page.goto(URL_ARCHIVES, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
                }
            }
        }

        if (echecsLocaux.length > 0) {
            console.log(`\n   🔄 RÉESSAI local des ${echecsLocaux.length} fichier(s)...`);
            const deuxiemeChance = [...echecsLocaux];
            echecsLocaux = [];

            for (const nomFichier of deuxiemeChance) {
                const cheminComplet = path.join(dossierActuel, nomFichier);
                try {
                    console.log(`\n   [2/2] Tentative de secours : ${nomFichier}`);
                    const infosExtraites = validerEtExtraireInfos(nomFichier);
                    await ecouterReseauEtMettreEnPause();
                    
                    await traiterFichier(page, cheminComplet, infosExtraites);

                    const cheminDossierSucces = path.join(dossierActuel, NOM_DOSSIER_SUCCES);
                    if (!fs.existsSync(cheminDossierSucces)) fs.mkdirSync(cheminDossierSucces);
                    fs.renameSync(cheminComplet, path.join(cheminDossierSucces, nomFichier));
                    
                    totalFichiersReussis++;
                    console.log(`      ✅ Succès au deuxième essai !`);
                    
                } catch (e) {
                    console.error(`      ❌ Échec définitif : ${nomFichier}`);
                    listeGlobaleEchecs.push(`[ÉCHEC TECHNIQUE] ${cheminComplet}`);
                    await page.goto(URL_ARCHIVES, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
                }
            }
        }
    } else {
        console.log(`   (Aucun PDF valide ici)`);
    }

    for (const nomSousDossier of sousDossiers) {
        await parcourirEtTraiterDossier(path.join(dossierActuel, nomSousDossier), page);
    }
}

// ==========================================
// 5. POINT DE LANCEMENT (MAIN)
// ==========================================
(async () => {
    console.log(`\n🚀 Lancement de l'automate intelligent (Département cible : ${DEPARTEMENT_CIBLE.label})...`);

    const browser = await chromium.launch({ headless: false, slowMo: 100 });
    const context = await browser.newContext();
    const page = await context.newPage();

    console.log("Vérification de l'accès et authentification...");
    await ecouterReseauEtMettreEnPause();
    await page.goto(URL_ARCHIVES, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => { });

    const emailInput = page.locator('input[name="email"]');
    if (await emailInput.count() > 0) {
        console.log("🔐 Authentification requise...");
        await emailInput.fill(user_login);
        await page.locator('input[name="password"]').fill(password);
        await page.locator('button:has-text("Connexion")').click();
        
        await page.waitForURL(URL_ARCHIVES, { timeout: 60000 });
        console.log("🔓 Connecté avec succès !");
    }

    await parcourirEtTraiterDossier(DOSSIER_RACINE, page);

    console.log("\n" + "=".repeat(70));
    console.log("📊 RAPPORT FINAL D'ARCHIVAGE");
    console.log("=".repeat(70));
    console.log(`✅ Total de fichiers intégrés et rangés : ${totalFichiersReussis}`);
    console.log(`❌ Total de fichiers ignorés ou en échec : ${listeGlobaleEchecs.length}`);

    if (listeGlobaleEchecs.length > 0) {
         console.log("\n⚠️ Détail des anomalies (fichiers restés à leur place) :");
         listeGlobaleEchecs.forEach(chemin => console.log(`   - ${chemin}`));
    }
    console.log("=".repeat(70));

    if (totalFichiersReussis > 0) {
        const cheminFichierStats = path.join(__dirname, 'statistique.txt');
        
        const dateActuelle = new Date();
        const dateAffichage = dateActuelle.toLocaleDateString();
        const heureAffichage = dateActuelle.toLocaleTimeString();
        
        const ligneStatistique = `[${dateAffichage} à ${heureAffichage}] - Fichiers chargés : ${totalFichiersReussis}\n`;
        
        try {
            fs.appendFileSync(cheminFichierStats, ligneStatistique, 'utf8');
            console.log(`\n📝 Statistiques de session enregistrées dans : ${cheminFichierStats}`);
        } catch (erreur) {
            console.error(`\n❌ Impossible d'écrire dans le fichier de statistiques :`, erreur.message);
        }
    }

    console.log("\n🛑 Mission terminée.");
    await browser.close();
})();