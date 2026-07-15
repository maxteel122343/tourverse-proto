/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { FileCode2, Download } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-[#050507] text-white font-sans flex items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-[#0a0a0c] rounded-2xl shadow-xl border border-white/10 p-8 relative overflow-hidden">
        {/* Ambient glow effect in background */}
        <div className="absolute -top-[100px] -right-[100px] w-64 h-64 bg-blue-600/20 blur-[100px] rounded-full pointer-events-none"></div>
        <div className="absolute -bottom-[100px] -left-[100px] w-64 h-64 bg-purple-600/20 blur-[100px] rounded-full pointer-events-none"></div>

        <div className="relative z-10 flex items-center gap-4 mb-8">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <FileCode2 size={28} className="text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
              Tourverse <span className="text-blue-400 font-medium text-lg">Gemini</span>
            </h1>
            <p className="text-xs text-blue-400 font-medium uppercase tracking-tighter mt-1">Protótipo Python Gerado com Sucesso</p>
          </div>
        </div>

        <div className="relative z-10 text-gray-200 text-sm leading-relaxed mb-8">
          <p className="bg-white/5 p-4 rounded-xl border border-white/5">
            Os arquivos do protótipo em <strong className="text-white">Python / Gradio</strong> que você solicitou foram gerados no explorador de arquivos deste projeto (no menu lateral esquerdo).
          </p>
          
          <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mt-8 mb-4">Arquivos Gerados</h3>
          <ul className="space-y-3">
            {[
              { name: 'main.py', desc: 'Interface gráfica usando Gradio, yt-dlp e gerador de áudio.' },
              { name: 'gemini_guide.py', desc: 'Lógica do chat contínuo com o modelo gemini-1.5-pro.' },
              { name: 'prompts.py', desc: 'System prompt imersivo para o guia virtual brasileiro.' },
              { name: 'requirements.txt', desc: 'Lista de dependências necessárias do Python.' },
              { name: 'INSTRUCOES.md', desc: 'Passo a passo de como rodar o app localmente.' }
            ].map((file) => (
              <li key={file.name} className="flex items-center gap-4 p-3 bg-white/5 rounded-xl border border-white/5 shadow-sm transition-colors hover:bg-white/10">
                <span className="font-mono text-blue-300 font-medium whitespace-nowrap min-w-[140px] text-[11px] px-2.5 py-1 bg-black/40 rounded-md border border-white/5 tracking-tight">{file.name}</span>
                <span className="text-gray-300 text-sm leading-tight">{file.desc}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="relative z-10 mt-8 p-5 bg-blue-900/20 border border-blue-500/20 rounded-xl flex gap-4 shadow-inner">
          <div className="text-blue-400 mt-0.5 shrink-0">
            <Download size={20} />
          </div>
          <div className="text-sm text-blue-100/80 leading-relaxed">
            <strong className="text-blue-50 uppercase text-xs tracking-wider font-bold mb-1 block">Como rodar?</strong>
            Esta plataforma roda aplicativos web (Node.js). Para rodar seu projeto Python localmente, clique no ícone de opções (três pontos) no canto superior direito do AI Studio e selecione <strong className="text-blue-100">"Export as ZIP"</strong>, ou simplesmente copie o conteúdo dos arquivos listados. Leia o arquivo <code className="px-1.5 py-0.5 bg-black/40 rounded text-blue-300 font-mono text-xs border border-blue-500/20">INSTRUCOES.md</code> para ver como executar.
          </div>
        </div>
      </div>
    </div>
  );
}
