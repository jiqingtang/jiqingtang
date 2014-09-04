let g:Tlist_Show_One_File=1
let g:Tlist_Use_Right_Window=1
let g:Tlist_Exit_OnlyWindow=1
let g:Tlist_File_Fold_Auto_Close=1
let g:Tlist_Ctags_Cmd='ctags58'
let g:tlist_php_settings='php;c:class;i:interface;d:constant;f:function'
nnoremap <silent> <F8> :update<CR>:TlistToggle<CR>
inoremap <silent> <F8> <ESC><F8>

nnoremap <silent> <F7> :update<CR>:NERDTreeToggle<CR>
inoremap <silent> <F7> <ESC><F7>

nnoremap <silent> <F11> :call MarkCurrentWordWithNextColor()<CR>
inoremap <silent> <F11> <ESC><F11>

let g:miniBufExplModSelTarget = 1
nnoremap <silent> <F12> :TMiniBufExplorer<CR>
inoremap <silent> <F12> <ESC><F12>

set noswapfile
map ,f [I:let nr = input("Which one: ")<Bar>exe "normal " . nr ."[\t"<CR>

autocmd! FileType c,cpp,java,php,python,vim,javascript autocmd BufWritePre
    \ <buffer> :%s/\s\+$//e
autocmd FileType c,cpp,java,php,python,vim,javascript autocmd BufWritePre
    \ <buffer> :%s/\n\+\%$//e

autocmd BufRead,BufNewFile TARGETS setfiletype python

set complete=.,w,b,u
set hls
