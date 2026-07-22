const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const http = require('http');

// --- CONFIGURATION ---
const DOSSIER_RACINE = "/run/media/edithson/Ventoy/DCOB Fichiers/DCOB GAUS/Beta";
const NOM_DOSSIER_SUCCES = 'Fichiers_Archives_Succes';
const URL_ARCHIVES = 'http://172.20.9.254:8000/archives';

// --- DICTIONNAIRE INTELLIGENT ---
const DICTIONNAIRE_NATURES = {
    'DECI': 'DECISIONS',
    'FD': 'FONDS DE DOSSIER',
    'ESD': 'ESD',
    'NOTE': 'NOTE',
    'COMMUNIQUE': 'COMMUNIQUES',
    'CONVOCATION': 'CONVOCATIONS',
    'COURA': 'COURRIERS',
    'ST': 'SOIT-TRANSMIS',
    'SOIT': 'SOIT-TRANSMIS',
    'INVITATION': 'INVITATIONS',
    'COURRIERS': 'COURRIERS',
    'ATTESTATION': 'ATTESTATIONS',
    'MARCHE': 'MARCHE',
    'INSTRUCTIONS': 'INSTRUCTIONS',
    'CONSTITUTION': 'CONSTITUTION',
    'LOI': 'LOI',
    'LETTRE-DE-MISSION': 'LETTRE DE MISSION',
    'ARRETE': 'ARRETE',
    'DECRET': 'DECRET',
    'DOSSIER-DU-PERSONNEL': 'DOSSIER DU PERSONNEL',
    'DOSSIER-DES-PENSIONS': 'DOSSIER DES PENSIONS',
    'RAPPORTS': 'RAPPORTS',
    'DECISIONS': 'DECISIONS',
    'FONDS-DE-DOSSIER': 'FONDS DE DOSSIER',
    'LETTRE': 'LETTRE DE MISSION',
    'RAPPORT': 'RAPPORTS',
    'FICHE': 'DOSSIER DU PERSONNEL',
    'CERTIF': 'DOSSIER DU PERSONNEL',
    'BE': 'BONS D\'ENGAGEMENT',
    'COMPTE': 'COMPTE RENDU',
    'DECISION': 'DECISIONS',
    'DEMANDE': 'DEMANDES',
    'LETTRE': 'LETTRE DE MISSION',
    'MEMO': 'MEMO',
    'ACCOMPAGNEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'ACCORD': 'AUTRES TYPES DE DOCUMENTS',
    'ACCREDITATION': 'AUTRES TYPES DE DOCUMENTS',
    'ACHAT': 'AUTRES TYPES DE DOCUMENTS',
    // --- Nouveaux ajouts ---
    'ALLEGATIONS': 'AUTRES TYPES DE DOCUMENTS',
    'AMBASSADE': 'AUTRES TYPES DE DOCUMENTS',
    'ANNEXE': 'AUTRES TYPES DE DOCUMENTS',
    'ANNEXES': 'AUTRES TYPES DE DOCUMENTS',
    'APPENDIX': 'AUTRES TYPES DE DOCUMENTS',
    'APPLICATION': 'AUTRES TYPES DE DOCUMENTS',
    'APPUI': 'AUTRES TYPES DE DOCUMENTS',
    'ATTRIBUTION': 'AUTRES TYPES DE DOCUMENTS',
    'AUTORISATION': 'AUTRES TYPES DE DOCUMENTS',
    'BORDEREAU': 'AUTRES TYPES DE DOCUMENTS',
    'BUDGET': 'AUTRES TYPES DE DOCUMENTS',
    'BUDGETISATION': 'AUTRES TYPES DE DOCUMENTS',
    'CAHIER': 'AUTRES TYPES DE DOCUMENTS',
    'CAPTURE': 'AUTRES TYPES DE DOCUMENTS',
    'CERTIFICAT': 'CERTIFICATS',      // ← cohérent avec 'CERTIF'
    'CIRCULAIRE': 'AUTRES TYPES DE DOCUMENTS',
    'CIRCULAR': 'AUTRES TYPES DE DOCUMENTS',
    'CLOTURE': 'AUTRES TYPES DE DOCUMENTS',
    'CONFRERENCE': 'AUTRES TYPES DE DOCUMENTS',
    'CONTINUITE': 'AUTRES TYPES DE DOCUMENTS',
    'COORDINATION': 'AUTRES TYPES DE DOCUMENTS',
    'CREATION': 'AUTRES TYPES DE DOCUMENTS',
    'DATE': 'AUTRES TYPES DE DOCUMENTS',
    'DEMANE': 'DEMANDES',                       // ← typo de DEMANDE
    'DENONCIATION': 'AUTRES TYPES DE DOCUMENTS',
    'DEPLOIEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'DEPOTS': 'AUTRES TYPES DE DOCUMENTS',
    'DEROGATION': 'AUTRES TYPES DE DOCUMENTS',
    'DESIGNATION': 'AUTRES TYPES DE DOCUMENTS',
    'DIALOGUE': 'AUTRES TYPES DE DOCUMENTS',
    'DOCUMENTS': 'AUTRES TYPES DE DOCUMENTS',
    'EDITION': 'AUTRES TYPES DE DOCUMENTS',
    'ENTREVUE': 'AUTRES TYPES DE DOCUMENTS',
    'ETAT': 'AUTRES TYPES DE DOCUMENTS',
    'EXECUTION': 'AUTRES TYPES DE DOCUMENTS',
    'EXTENSION': 'AUTRES TYPES DE DOCUMENTS',
    'FINANCEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'FODECC': 'AUTRES TYPES DE DOCUMENTS',
    'FONCTIONNEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'FORMATION': 'AUTRES TYPES DE DOCUMENTS',
    'IMPREGNATION': 'AUTRES TYPES DE DOCUMENTS',
    'INFORMATION': 'AUTRES TYPES DE DOCUMENTS',
    'INSTRUCTION': 'INSTRUCTIONS',              // ← cohérent avec 'INSTRUCTIONS'
    'INVENTAIRE': 'AUTRES TYPES DE DOCUMENTS',
    'INVITATAION': 'INVITATIONS',               // ← typo de INVITATION
    'LANCEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'LAW': 'LOI',                               // ← équivalent anglais de LOI
    'LIVRAISON': 'AUTRES TYPES DE DOCUMENTS',
    'MAIL': 'AUTRES TYPES DE DOCUMENTS',                        // ← assimilé courrier
    'MESURES': 'AUTRES TYPES DE DOCUMENTS',
    'MINUTES': 'AUTRES TYPES DE DOCUMENTS',
    'MISE': 'AUTRES TYPES DE DOCUMENTS',
    'MISSION': 'LETTRE DE MISSION',             // ← cohérent avec 'LETTRE'
    'NASLA': 'AUTRES TYPES DE DOCUMENTS',
    'NON': 'AUTRES TYPES DE DOCUMENTS',
    'NOTIFICATION': 'AUTRES TYPES DE DOCUMENTS',
    'OBSERVATION': 'AUTRES TYPES DE DOCUMENTS',
    'OUVERTURE': 'AUTRES TYPES DE DOCUMENTS',
    'PAIEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'PRIOR': 'AUTRES TYPES DE DOCUMENTS',
    'PROBLEMATIQUE': 'AUTRES TYPES DE DOCUMENTS',
    'PROCURATION': 'AUTRES TYPES DE DOCUMENTS',
    'PRODUCTION': 'AUTRES TYPES DE DOCUMENTS',
    'PROJET': 'AUTRES TYPES DE DOCUMENTS',
    'PROROGATION': 'AUTRES TYPES DE DOCUMENTS',
    'PROTOCOLE': 'AUTRES TYPES DE DOCUMENTS',
    'PV': 'PROCES-VERBAL',                       // ← Procès-Verbal ≈ compte rendu
    'RAPORT': 'RAPPORTS',                       // ← typo de RAPPORT
    'RAPPEL': 'AUTRES TYPES DE DOCUMENTS',
    'RECLAMATION': 'AUTRES TYPES DE DOCUMENTS',
    'RECLASSEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'RECOUVREMENT': 'AUTRES TYPES DE DOCUMENTS',
    'RELANCE': 'AUTRES TYPES DE DOCUMENTS',
    'REMUNERATION': 'AUTRES TYPES DE DOCUMENTS',
    'REPONSE': 'AUTRES TYPES DE DOCUMENTS',
    'REPONSES': 'AUTRES TYPES DE DOCUMENTS',
    'REPORT': 'AUTRES TYPES DE DOCUMENTS',
    'REPRISE': 'AUTRES TYPES DE DOCUMENTS',
    'REQUETE': 'AUTRES TYPES DE DOCUMENTS',
    'RETABLISSEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'RETRAIT': 'AUTRES TYPES DE DOCUMENTS',
    'REUNION': 'AUTRES TYPES DE DOCUMENTS',
    'REVERSEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'SEMINAIRE': 'AUTRES TYPES DE DOCUMENTS',
    'SITUATION': 'AUTRES TYPES DE DOCUMENTS',
    'STAGE': 'AUTRES TYPES DE DOCUMENTS',
    'SYNTHESE': 'AUTRES TYPES DE DOCUMENTS',
    'TERMES': 'AUTRES TYPES DE DOCUMENTS',
    'TRAITEMENT': 'AUTRES TYPES DE DOCUMENTS',
    'TRANSMISSION': 'AUTRES TYPES DE DOCUMENTS',
    'TRAVAUX': 'AUTRES TYPES DE DOCUMENTS',
    'VISA': 'AUTRES TYPES DE DOCUMENTS',
};

const VALEURS_AUTORISEES = [
    "ATTESTATIONS", "MARCHE", "COMMUNIQUES", "COMPTE RENDU", "DEMANDES",
    "SOIT-TRANSMIS", "CONVOCATIONS", "COURRIERS", "INVITATIONS",
    "INSTRUCTIONS", "CONSTITUTION", "LOI", "LETTRE DE MISSION", "ARRETE",
    "DECRET", "DOSSIER DU PERSONNEL", "ESD", "DOSSIER DES PENSIONS",
    "RAPPORTS", "NOTE", "DECISIONS", "FONDS DE DOSSIER", "BONS D'ENGAGEMENT",
    "MEMO", "AUTRES TYPES DE DOCUMENTS", "CERTIFICATS", "PROCES-VERBAL"
];

let totalFichiersReussis = 0;
let listeGlobaleEchecs = [];

// ==========================================
// 1. MODULE DE VALIDATION ET D'EXTRACTION
// ==========================================
function validerEtExtraireInfos(nomFichier) {
    // CORRECTION ICI : Retire ".pdf" ou ".PDF" sans distinction
    const nomSansExt = nomFichier.replace(/\.pdf$/i, '');
    const parts = nomSansExt.split(' '); //modif ici

    if (parts.length < 3) {
        throw new Error("STRUCTURE_INVALIDE: Manque d'informations (pas de tirets '_').");
    }

    const prefix = parts[0];
    const natureDocument = DICTIONNAIRE_NATURES[prefix] || prefix;

    if (!VALEURS_AUTORISEES.includes(natureDocument)) {
        throw new Error(`STRUCTURE_INVALIDE: Nature de document non autorisée ou inconnue ('${prefix}').`);
    }

    const dateStr = parts[parts.length - 1];
    if (!/^\d{8}$/.test(dateStr)) {
        throw new Error(`STRUCTURE_INVALIDE: La fin du fichier ('${dateStr}') n'est pas une date à 8 chiffres.`);
    }

    const jour = dateStr.substring(0, 2);
    const mois = dateStr.substring(2, 4);
    const annee = dateStr.substring(4, 8);

    return {
        natureDocument,
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
// 3. FONCTION CORE : UPLOAD
// ==========================================
async function traiterFichier(page, cheminComplet, infosFichier) {
    await page.goto(URL_ARCHIVES, { waitUntil: 'networkidle', timeout: 120000 });
    await page.waitForSelector('select[name="format"]', { timeout: 90000 });

    await page.locator('select[name="format"]').selectOption('Document PDF', { force: true });
    await page.locator('select:has(option[value="INSTRUCTIONS"])').selectOption(infosFichier.natureDocument, { force: true });
    await page.locator('#description').fill(infosFichier.nomSansExt);
    await page.locator('#date_doc').fill(infosFichier.dateFormatee);
    await page.locator('select:has(option[value="FOUDA"])').selectOption('FOUDA', { force: true });
    await page.locator('select[name="emplacement2"]').selectOption('Serveur', { force: true });
    await page.locator('#rayon').fill('B6');
    await page.locator('#cote').fill('C1560-40DE.10');
    await page.locator('select:has(option[value="DCOB"])').selectOption('DCOB', { force: true });

    await page.locator('button:has-text("Suivant")').click();

    await page.waitForSelector('#file', { state: 'visible', timeout: 90000 });
    await page.locator('#file').setInputFiles(cheminComplet);
    await page.locator('button:has-text("Suivant")').click();

    await page.waitForSelector('button:has-text("Valider")', { timeout: 90000 });
    console.log("      -> Étape 3 : Validation... (Attente réseau : max 180s)");

    const reponseServeur = page.waitForResponse(
        response => response.request().method() !== 'GET' && response.status() >= 200 && response.status() < 400,
        { timeout: 180000 }
    );

    await page.locator('button:has-text("Valider")').click();
    await reponseServeur;

    console.log("      -> ✅ Upload confirmé par le serveur !");
    await page.waitForTimeout(1500);
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
            // CORRECTION ICI : .toLowerCase() pour matcher .pdf ou .PDF
        } else if (el.isFile() && el.name.toLowerCase().endsWith('.pdf')) {
            fichiersPDF.push(el.name);
        }
    }

    if (fichiersPDF.length > 0) {
        console.log(`   📄 ${fichiersPDF.length} fichier(s) PDF trouvé(s).`);

        let echecsLocaux = [];
        let succesLocaux = [];

        for (const nomFichier of fichiersPDF) {
            const cheminComplet = path.join(dossierActuel, nomFichier);
            try {
                console.log(`\n   [1/2] Analyse : ${nomFichier}`);

                const infosExtraites = validerEtExtraireInfos(nomFichier);
                await ecouterReseauEtMettreEnPause();
                await traiterFichier(page, cheminComplet, infosExtraites);
                succesLocaux.push(nomFichier);

            } catch (e) {
                if (e.message.startsWith('STRUCTURE_INVALIDE')) {
                    console.error(`      ❌ Rejeté (Format Invalide) : ${e.message.replace('STRUCTURE_INVALIDE: ', '')}`);
                    listeGlobaleEchecs.push(`[FORMAT INVALIDE] ${cheminComplet}`);
                } else {
                    console.error(`      ⚠️ Échec (Timeout/Réseau) : ${e.message.split('\n')[0]}`);
                    echecsLocaux.push(nomFichier);
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

                    succesLocaux.push(nomFichier);
                    console.log(`      ✅ Succès au deuxième essai !`);
                } catch (e) {
                    console.error(`      ❌ Échec définitif : ${nomFichier}`);
                    listeGlobaleEchecs.push(`[ÉCHEC TECHNIQUE] ${cheminComplet}`);
                }
            }
        }

        if (succesLocaux.length > 0) {
            const cheminDossierSucces = path.join(dossierActuel, NOM_DOSSIER_SUCCES);
            if (!fs.existsSync(cheminDossierSucces)) fs.mkdirSync(cheminDossierSucces);

            for (const fichier of succesLocaux) {
                const ancienChemin = path.join(dossierActuel, fichier);
                const nouveauChemin = path.join(cheminDossierSucces, fichier);
                try {
                    fs.renameSync(ancienChemin, nouveauChemin);
                } catch (err) { }
            }
            totalFichiersReussis += succesLocaux.length;
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
    console.log(`\n🚀 Lancement de l'automate intelligent...`);

    const browser = await chromium.launch({ headless: false, slowMo: 100 });
    const context = await browser.newContext();
    const page = await context.newPage();

    console.log("Vérification de l'accès et authentification...");
    await ecouterReseauEtMettreEnPause();
    await page.goto(URL_ARCHIVES, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => { });

    const emailInput = page.locator('input[name="email"]');
    if (await emailInput.count() > 0) {
        console.log("🔐 Authentification requise...");
        await emailInput.fill('archive@mail.com');
        await page.locator('input[name="password"]').fill('OOOOO');
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

    // if (listeGlobaleEchecs.length > 0) {
    //     console.log("\n⚠️ Détail des anomalies (fichiers restés à leur place) :");
    //     listeGlobaleEchecs.forEach(chemin => console.log(`   - ${chemin}`));
    // }
    console.log("=".repeat(70));

    console.log("\n🛑 Mission terminée.");
    await browser.close();
})();